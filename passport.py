from mrz.generator.td3 import TD3CodeGenerator

code = TD3CodeGenerator("P", "FRA", "THOMAS", "AALDENBERG", "FE4908165", "FRA", "971007", "M", "250812","")
code = TD3CodeGenerator("P", "FRA", "THOMAS", "AALDENBERG", "FK8149005", "FRA", "971007", "M", "250812","")

code = TD3CodeGenerator("P", "FRA", "THOMAS", "AALDENBERG", "AF2289005", "FRA", "971007", "M", "250812","")

code = TD3CodeGenerator("P", "FRA", "THOMAS", "AALDENBERG", "XP2831245", "FIN", "971007", "M", "250812","")

code = TD3CodeGenerator("P", "FRA", "monotanabe", "AALDENBERG", "AF3158240", "FIN", "971007", "M", "250812","")

print(code)