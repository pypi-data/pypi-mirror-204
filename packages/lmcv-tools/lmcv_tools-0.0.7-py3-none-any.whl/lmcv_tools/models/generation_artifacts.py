class Artifact:
   def __init__(self, name: str, file_extension: str, data: str = ''):
      self.name = name
      self.file_extension = file_extension
      self.data = data
   
   @property
   def file_name(self) -> str:
      return self.name + '.' + self.file_extension
   
   # Para Implementar
   def generate(self):
      return self.data

class Material:
   def __init__(self, elastic_modulus: float, poisson_coefficient: float, density: float) -> None:
      self.E = elastic_modulus
      self.nu = poisson_coefficient
      self.pho = density

      # Calculando Módulo Volumétrico
      self.K = self.E / (3 * (1 - 2 * self.nu))

      # Calculando Módulo de Cisalhamento
      self.G = self.E / (2 * (1 + self.nu))

class MicromechanicalModel:
   # Funções de Homogeneização Privadas
   def _voight(self, volume_fractions: list[float]):
      E, nu, pho = 0, 0, 0
      for V, M in zip(volume_fractions, self.materials):
         E += V * M.E
         nu += V * M.nu
         pho += V * M.pho
      return E, nu, pho

   def _mori_tanaka(self, volume_fractions: list[float]):
      # Definindo Valores Especiais
      V, M = volume_fractions, self.materials
      V1, V2 = V[0], V[1]
      K1, K2 = M[0].K, M[1].K
      G1, G2 = M[0].G, M[1].G
      FG = (G1 * (9 * K1 + 8 * G1)) / (6 * (K1 + 2 * G1))
      FK = 4 * G1 / 3

      # Calculando Módulo Volumétrico
      K = K1 + V2 / ((1 / (K2 - K1)) + (V1 / (K1 + FK)))

      # Calculando Módulo de Cisalhamento
      G = G1 + V2 / ((1 / (G2 - G1)) + (V1 / (G1 + FG)))

      # Calculando Propriedades Efetivas
      E = (9 * K * G) / (3 * K + G)
      nu = (3 * K - 2 * G) / (2 * (3 * K + G))

      # Densidade Calculada pelo Modelo de Voight
      pho = V1 * M[0].pho + V2 * M[1].pho

      return E, nu, pho

   # Relação Modelo/Função de Homogeneização
   homogenize_functions = {
      'voight': _voight,
      'mori_tanaka': _mori_tanaka
   }

   def __init__(self, name: str, materials: list[Material]) -> None:
      self.name = name
      self.materials = materials
      try:
         self._homogenize = MicromechanicalModel.homogenize_functions[name]
      except KeyError:
         raise ValueError(f'Micromechanical Model "{name}" is not supported.')
   
   def homogenize(self, volume_fractions: list[float]):
      return self._homogenize(self, volume_fractions)

class ElementConfiguration:
   # Elementos Suportados
   supported_types = {'Solid', 'Shell'}

   def __init__(self, type: str, number_integration_points: int):
      if type not in ElementConfiguration.supported_types:
         raise ValueError(f'Element Type "{type}" is not supported.')
      self.type = type
      self.number_integration_points = number_integration_points

class VirtualLaminas(Artifact):
   def __init__(
      self,
      laminas_count: int,
      thickness: float,
      power_law_exponent: float,
      element_configuration: ElementConfiguration,
      micromechanical_model: MicromechanicalModel,
      smart: bool = False
   ):
      super().__init__('virtual_laminas', 'inp')
      self.laminas_count = laminas_count
      self.thickness = thickness
      self.power_law_exponent = power_law_exponent
      self.element_configuration = element_configuration
      self.micromechanical_model = micromechanical_model
      self.smart = smart
   
   def volume_fraction(self, z: float):
      return (1 - z) ** self.power_law_exponent
   
   def z_coordinate(self, V: float):
      return 1 - V ** (1 / self.power_law_exponent)

   def equally_thickness_laminas(self):
      step = 1 / self.laminas_count
      points = [step / 2 + i * step for i in range(self.laminas_count)]
      fractions = [self.volume_fraction(z) for z in points]
      if self.element_configuration.type == 'Solid':
         thickness = [self.thickness for _ in range(self.laminas_count)]
      else:
         thickness = [step * self.thickness for _ in range(self.laminas_count)]
      return fractions, thickness

   def smart_laminas(self):
      # Variáveis Iniciais
      n = self.laminas_count
      p = self.power_law_exponent
      V = self.volume_fraction
      z = self.z_coordinate
      fractions_z = list()
      fractions_V = list()
      thickness_z = list()
      thickness_V = list()
      
      # Calculando Z de Referência
      if p == 1:
         z_ref = 0.5
      else:
         z_ref = 1 - p ** (-1 / (p - 1))
      
      # Decidindo se a Região de Prioridade z está à Esquerda ou Direita
      V_ref = V(z_ref)
      slope_tendency = p * (p - 1) * (1 - z_ref) ** (p - 2)
      if slope_tendency > 0:
         l_V = 1 - V_ref
         l_z = 1 - z_ref
      else:
         l_V = V_ref
         l_z = z_ref

      # Parâmetros da Região de Prioridade V
      n_V = round(l_z * n)
      step_V = l_V / n_V
      if slope_tendency > 0:
         z_0 = 0
         V_i = 1 - step_V / 2
      else:
         z_0 = z_ref
         V_i = V_ref - step_V / 2

      # Gerando Laminas da Região de Prioridade V 
      for _ in range(n_V):
         # Calculando Espessura Variável
         h_i = z(V_i - step_V / 2) - z_0

         # Registrando Informações
         fractions_V.append(V_i)
         thickness_V.append(h_i)

         # Atualizando Fração de Volume e Referência para Espessura
         V_i -= step_V
         z_0 += h_i
      
      # Parâmetros da Região de Prioridade z
      n_z = n - n_V
      step_z = l_z / n_z
      if slope_tendency > 0:
         z_i = z_ref + step_z / 2
      else:
         z_i = step_z / 2

      # Gerando Laminas da Região de Prioridade z
      for _ in range(n_z):
         fractions_z.append(V(z_i))
         thickness_z.append(step_z)
         z_i += step_z
      
      # Mesclando Regiões
      if slope_tendency > 0:
         fractions = fractions_V + fractions_z
         thickness = thickness_V + thickness_z
      else:
         fractions = fractions_z + fractions_V
         thickness = thickness_z + thickness_V

      # Corrigindo Espessura
      thickness = [t * self.thickness for t in thickness]

      return fractions, thickness

   def generate(self):
      # Inicializando Dados
      inp_data = ''

      # Gerados Dados de Lâminas
      laminas = self.smart_laminas() if self.smart else self.equally_thickness_laminas()

      # Escrevendo Materiais
      material_names = list()
      index = 1
      for V in laminas[0]:
         # Gerando e Armazando Nome de Material
         name =  f'FGM-L{index}'
         material_names.append(name)

         # Homogeneizando Propriedades
         E, nu, pho = self.micromechanical_model.homogenize([V, 1 - V])

         # Adicionando Dados
         inp_data += f'*Material, name={name}\n    *Density\n    {pho:.3f},\n    *Elastic\n    {E:.3f}, {nu:.3f}\n'
         
         index += 1
      
      # Preparando para Escrever Lâminas
      inp_data += '*Part, name=Virtual_Part\n*Node\n    1, 1.0, 1.0, 0.0\n    2, 0.0, 1.0, 0.0\n    3, 0.0, 0.0, 0.0\n    4, 1.0, 0.0, 0.0\n*Element, type=S4R\n    1, 1, 2, 3, 4\n*Elset, elset=Virtual\n    1'
      element_type = self.element_configuration.type
      int_points = self.element_configuration.number_integration_points
      rotation_angle = 0

      # Escrevendo Lâmina por Lâmina
      inp_data += f'\n*{element_type} Section, elset=Virtual, composite\n'
      index = 1
      for h, material in zip(laminas[1], material_names):
         inp_data += f'    {h:.11E}, {int_points}, {material}, {rotation_angle}, Ply-{index}\n'
         index += 1
      inp_data += '*End Part'

      # Inseridos dados Inp no Atributo de Dados
      self.data = inp_data