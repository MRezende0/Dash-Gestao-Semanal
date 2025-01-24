import requests

# Função para obter o token de acesso
def obter_token():
    # Token obtido no Graph Explorer
    ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJub25jZSI6Ikt3LTgwNnpRTlNWUHNQVG5vMTl5cGNGa004YkR0NXVRQzloQ09iOGdTSzgiLCJhbGciOiJSUzI1NiIsIng1dCI6IllUY2VPNUlKeXlxUjZqekRTNWlBYnBlNDJKdyIsImtpZCI6IllUY2VPNUlKeXlxUjZqekRTNWlBYnBlNDJKdyJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC85YjRmYjk5MC1jNDc0LTQ5YmEtYWVlYi0wZWExNTI3MGIyOWEvIiwiaWF0IjoxNzM3NzIxNDU0LCJuYmYiOjE3Mzc3MjE0NTQsImV4cCI6MTczNzgwODE1NCwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhaQUFBQTRsUWoycFNIWUJ3REpiR2VsYlVzWnFQODlrVXI4cUFIa1FzU1BvZW9RY1VDc2tIVGtUdHNrN0dhK29va0VqQjBoa2I0RlQwZThLeFpod01OTkxUaE82Y3RxY1UzWVBLaVBrV1N5QnJTbmFJPSIsImFtciI6WyJwd2QiLCJtZmEiXSwiYXBwX2Rpc3BsYXluYW1lIjoiR3JhcGggRXhwbG9yZXIiLCJhcHBpZCI6ImRlOGJjOGI1LWQ5ZjktNDhiMS1hOGFkLWI3NDhkYTcyNTA2NCIsImFwcGlkYWNyIjoiMCIsImNhcG9saWRzX2xhdGViaW5kIjpbIjRiMzZjZDJlLTZhOTItNDk0MS1hZDQ2LWI1MjczZTc0ZjVmMiJdLCJmYW1pbHlfbmFtZSI6IlByZXppYSBSZXplbmRlIiwiZ2l2ZW5fbmFtZSI6Ik1hdGhldXMiLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIxNzcuMTI0LjY2LjE2MiIsIm5hbWUiOiJNYXRoZXVzIFByZXppYSBSZXplbmRlIiwib2lkIjoiZjhjYWQ5NmEtNmQ3Yy00YjE4LWI2ZTItOTNkZjM1YzMyMGZkIiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTQ5NzUwMTI0NS0xMzczMjAwOTQ5LTE1NTY4OTk0OTYtMjE2NjEiLCJwbGF0ZiI6IjMiLCJwdWlkIjoiMTAwMzIwMDM2QzExNDUyOCIsInJoIjoiMS5BU1lBa0xsUG0zVEV1a211Nnc2aFVuQ3ltZ01BQUFBQUFBQUF3QUFBQUFBQUFBQW1BRkltQUEuIiwic2NwIjoiRGlyZWN0b3J5LlJlYWQuQWxsIERpcmVjdG9yeS5SZWFkV3JpdGUuQWxsIEdyb3VwLlJlYWQuQWxsIEdyb3VwLlJlYWRXcml0ZS5BbGwgR3JvdXBNZW1iZXIuUmVhZC5BbGwgb3BlbmlkIHByb2ZpbGUgU2l0ZXMuUmVhZC5BbGwgU2l0ZXMuUmVhZFdyaXRlLkFsbCBVc2VyLlJlYWQgZW1haWwiLCJzaWQiOiIwMDEyZjNhOS00NDUwLTFlOTItMGMxOC00NWNhMTA1NzE5NDgiLCJzaWduaW5fc3RhdGUiOlsiaW5rbm93bm50d2siXSwic3ViIjoiUzRJUXQzQ3VTekVjUFFBejRmTFBaWGhhNGVuSlZ2NXhJcGNBN01WOTZBVSIsInRlbmFudF9yZWdpb25fc2NvcGUiOiJTQSIsInRpZCI6IjliNGZiOTkwLWM0NzQtNDliYS1hZWViLTBlYTE1MjcwYjI5YSIsInVuaXF1ZV9uYW1lIjoibWF0aGV1cy5yZXplbmRlQGNvY2FsLmNvbS5iciIsInVwbiI6Im1hdGhldXMucmV6ZW5kZUBjb2NhbC5jb20uYnIiLCJ1dGkiOiJXd3ZVS09hWW1VaURFSjBIQzU5WUFBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX2NjIjpbIkNQMSJdLCJ4bXNfZnRkIjoiUWt1bElEaWZTZEZrUldwREx5d1FVdDQzNjVzX2ZnRGdIakNpcUhmZDF5SSIsInhtc19pZHJlbCI6IjEgMzAiLCJ4bXNfc3NtIjoiMSIsInhtc19zdCI6eyJzdWIiOiJWRk5jOWRES2tjNUNXYVFvN3JkcWFtV2dwRGpFWmZ1YnMyRmRKU0Q4aXdrIn0sInhtc190Y2R0IjoxNTM1MTE0NTEzfQ.D_BSQf592QeaiXWu-q3r5mVBK3_CBYQwXFbcIYAcG2ddONKNUr0GwQqtZCd1NmdF7Kn8HlncbSWvM1L9Nk9AMkLwWt0wZtJ2YIBE1CNJuI5Sy_3Y0FTSlXqgIjgVwiCD95K7yplS6SPYBQTocxbJJg2RuLGE2WH-PzHBRoXmBLRWrxMwgn8M-BUePTkoHyZU8hKYRfMwg4m6vD8fsi87nFLRJaahRY1qAtW4yHAu5ZBq5v3G8zLoVCHCdphafwO5YU-Y6QPONKFdmY1oOFItVSTlGMA4a03TzzgvXe8DWdn1VjnPocahOnaQ-zrlGh-6GXBNfk6fdj9wSwsBTeYmHQ"

    # Configurar cabeçalhos da requisição
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    return headers