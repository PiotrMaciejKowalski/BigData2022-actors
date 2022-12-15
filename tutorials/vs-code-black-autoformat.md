# Po co autoformatery

Bardzo często do tej pory pisaliśmy kod. Dużo częściej niż faktycznie go czytaliśmy. Pojawienie się 
review w naszym procesie projektowym zaczęło zaburzać tę proporcję. Nagle bowiem pojawia się potrzeba czytania i to nie swojego kodu. Efektem tego jest to, że indywidualne preferencje mogą powodować dodatkowy narzut pracy. Stworzono więc programy, których jedynym zadaniem jest tak poukładać bloki kodu, aby można je było łatwo czytać. 

Jednym z tych formaterów jest black. I poniżej w esencji podam jak wywołać blacka w połączeniu z vs-code. Moim źródłem jest tu link [https://marcobelo.medium.com/setting-up-python-black-on-visual-studio-code-5318eba4cd00](https://marcobelo.medium.com/setting-up-python-black-on-visual-studio-code-5318eba4cd00)

# Instalacja blacka

Black jest programem, ale nie pobiera się go zwyczajnie i instaluje jak każdy program. Jest aplikacją pobieraną wewnątrz środowiska pythona. Podobnie do jupytera. Należy zatem wybrać środowisko którego 
używamy w projekcie i wykonać operacje

```sh
pip install black
```

# Ustawienia w VS-code

Aby można było uruchomić autoformatowanie w pythonie VS-Code musi posiadać zainstalowany plugin do pythona. Choć pewnie mamy go już zainstalowanego omówmy i ten krok

* ctrl + p -> piszemy `ext install ms-python.python`
* wybieramy File->Preferences->Settings i szukamy opcji `format on save`. Jeśli jest wyłączona - włączamy
* w tym samym settings szukamy `python formatting provider` i wybieramy `black`

Na koniec uwaga. *Black* nie będzie w stanie autoformatować kodu z błędami składni. Aby autoformat sie powiódł trzeba je najpierw naprawić.