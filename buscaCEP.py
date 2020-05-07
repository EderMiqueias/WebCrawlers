from urllib.parse import urlencode
from urllib.request import Request, urlopen


# INFORMA UM ENDEREÇO A PARTIR DE UM CEP


def crawler(cep):
    url = "http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaEndereco.cfm"
    post_fields = {"CEP": cep}

    req = Request(url, urlencode(post_fields).encode())
    result = str(urlopen(req).read())

    def clearS1(s):
        s = s.replace(r"\t", '')
        s = s.replace(r"\n", '')
        s = s.replace(r"\r", '')
        return s

    def clearS2(s):
        inf = s[s.find("</tr>") + 6: s.find("</table>")]
        inf = inf.replace("tr>", '')
        inf = inf.replace("&nbsp", '')
        return inf

    result = bytes(result, "iso-8859-1").decode("unicode_escape")
    source_code = clearS1(result)

    table = source_code[
        source_code.find("<table"): source_code.find("</table>") + 8
    ]

    tr_infos = clearS2(table)
    tr_infos = tr_infos.split("</td>")
    tr_infos = tr_infos[:3]

    return tr_infos


if __name__ == "__main__":
    print("Correios Busca CEP - Endereço")
    while True:
        cep = input("\nCEP: ")
        if len(cep) != 8:
            break

        data = crawler(cep)
        labels = ("Logradouro/Nome: ", "Bairro/Distrito: ",
                  "Localidade/UF: ")

        aux = 0
        for x in data:
            print(labels[aux], end='')
            print(x[x.find(">") + 1:-1])
            aux += 1
