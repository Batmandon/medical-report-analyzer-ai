from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

print("List of models that support generateContent:\n")
for m in client.models.list():
    for action in m.supported_actions:
        if action == "generateContent":
            print(m.name)

print("List of models that support embedContent:\n")
for m in client.models.list():
    for action in m.supported_actions:
        if action == "embedContent":
            print(m.name)

# class Solution(object):
#     def romanToInt(self, s):
#         roman = {
#     'I': 1,
#     'V': 5,
#     'X': 10,
#     'L': 50,
#     'C': 100,
#     'D': 500,
#     'M': 1000
# }

#         prev = 0
#         total = 0

#         for char in reversed(s):
#             if char < prev:
#                 curr = roman[char]
#                 total -= curr
#             else:
#                 total += curr

#             prev = char

#         return total 