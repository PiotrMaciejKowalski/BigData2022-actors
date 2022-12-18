# Czym są git hooki

Przepływ operacji w gitcie jest dość dobrze znany i ustalony. Wykonujemy kolejno operacje `git add`, `git commit` `git pull` `git push`, etc. Co jednak jeśli chcielibyśmy aby w pewnych sytuacjach działo się coś dodatkowego?

Okazuje się, że taka potrzeba zdarza się nader często w większych projektach. Np. jeśli byśmy chcieli przy każdym commit sprawdzić czy kod przechodzi testy jednostkowe. Okazuje się, że odpowiedzią są na to 
tzw. git hooki. W każdym repozytorium wyciągniętym lokalnie można odszukać ukryty katalog `.git` gdzie przechowywane są dane o commitach i wersjach. Wśród nich znajduje się informacja o hookach.

```sh
ls .git/hooks/
applypatch-msg.sample      post-update.sample     pre-merge-commit.sample    pre-receive.sample
commit-msg.sample          pre-applypatch.sample  prepare-commit-msg.sample  push-to-checkout.sample
fsmonitor-watchman.sample  pre-push.sample        update.sample              pre-commit.sample      pre-rebase.sample
```

Każdy z plików sample to tylko szablon jak dany hook mógłby wyglądać + opis działania. Każdemu hookowi jest przypisana odpowiednia akcja. Najpopularniejszym hookiem jest pre-commit - który jak nazwa wskazuje wykona się przy akcji commit - ale poprzedzając sam commit. 

Aby używać konkretnego hooka należy wykonać 3 rzeczy:

* (prosta) utworzyć plik o nazwie hooka ale już bez .sample czy innego rozszerzenia,
* (prosta) nadać mu uprawnienia wykonywania (np. wykonując w terminalu `chmod +x hook`),
* (trudna) napisać skrypt z czynnościami do wykonania.

Na szczęście można często podpatrzeć hooki w internecie - które pomogą zapanować nad akcjami, które chcemy wykonywać. Poniżej wklejam hooka do zrzucania notatników jupytera do kodu pythonowego w katalogu stripped (po to go tworzyliśmy w szablonie):

```sh
#!/bin/bash -e
git diff --cached --name-only --diff-filter=ACM | while IFS='' read -r line || [[ -n "$line" ]]; do
  if [[ $line == *.ipynb ]] ;
  then
    nb_dir=$(dirname $line)
    if [[ $nb_dir == "." ]]; then
        nb_dir=""
    fi
    filename=$(basename $line)
    stripped_dir=stripped/${nb_dir} #copy the directory structure
    mkdir -p $stripped_dir
    target_stripped_file="${stripped_dir}/${filename%.ipynb}_stripped.py"
    jupyter nbconvert --to script $line --output "$(git rev-parse --show-toplevel)/${target_stripped_file%.py}" #nbconvert blindly adds the suffix .py to the filename...
    sed -i 's/\\n/\n/g' $target_stripped_file
    git add $target_stripped_file
  fi
done
```

# Problemy w użyciu hooków

Używanie hooków może prowadzić do problemów. Jednym z problemów powyższego hooka jest to, że jeśli terminal nie znajduje się obecnie z aktywowaną i poprawną conda to pewnie nie odszuka komendy `jupyter nbconvert`. To z kolei  może spowodować nieudane commitowanie. Należy wtedy posłużyć się linią komend (terminalem/consolą) gdzie aktywowane jest środowisko condy i pakiety jupytera są zainstalowane.

Dla przykładu ten terminal nie jest odpowiedni do takiego commitu

```
pkowalski@pkowalski-legion17:~/Workspace/projects/BigData2022-actors$

```
Natomiast kolejny po wykonaniu zapisanych tam kroków już jest

```
pkowalski@pkowalski-legion17:~/Workspace/projects/BigData2022-actors$ source /opt/anaconda3/bin/activate 
(base) pkowalski@pkowalski-legion17:~/Workspace/projects/BigData2022-actors$ conda activate bigdata
(bigdata) pkowalski@pkowalski-legion17:~/Workspace/projects/BigData2022-actors$
```