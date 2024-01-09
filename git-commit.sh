#!/bin/bash

echo "Commit 메시지와 파일을 입력하세요"
read -a commits
commit_cmd="git commit -m "
add_cmd="git add "

for ((idx=0; idx<${#commits[@]}; ++idx)); do
    if [ $idx -gt 0 ]
    then
        add_cmd+=" ${commits[idx]}"
    else
        commit_cmd+="${commits[idx]}"
    fi
done

echo `$add_cmd`
echo `$commit_cmd`
echo `git push`
echo "업데이트 완료!"

# for ELEMENT in 'Hydrogen' 'Helium' 'Lithium' 'Beryllium'; do
# for commit_file in ${commits[@]}; do
#     cmd+=" ${commit_file} "
# done

# echo "$VAR"
# VAR1="uname -o"
# echo `${VAR1}` 

#echo `uname -o`
# echo "Commit 할 파일을 입력하세요"
# read -a words
# for word in ${words[@]}; do
#     echo "${word}"
# done

# git add 
# git commit -m 'update'
# git push