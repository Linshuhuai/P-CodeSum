nohup python ../code/method/cli.py --pet_per_gpu_eval_batch_size 16 --pet_gradient_accumulation_steps 1 --pet_max_seq_length 512 --model_type roberta --model_name_or_path microsoft/codebert-base --embed_size 768 --task_name summary --data_dir ../data/h2o-3/train_500_10 --output_dir ../output/h2o-3/text-davinci-003/ptuning/Python_500_10_e100_ts1 --do_eval --eval_set test --pattern_ids 10 --pet_per_gpu_train_batch_size 5 --eval_every_step 5 --pet_repetitions 1 --show_limit 0 > ../output/h2o-3/text-davinci-003/ptuning/log_10/Python_500_10_e100_ts1_val.log
