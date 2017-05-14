for i in `ls results/evaluation`; do echo $i; python russe-evaluation/russe/evaluation/evaluate.py hj --hj_fpath=results/evaluation/$i; done
