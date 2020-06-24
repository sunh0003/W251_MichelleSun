
## Homework 09 Distributed High Performance Computation with GPUs

![Test Image 1](Eval_BLUE_score_1.png)

![Test Image 2](global_gradient_norm.png)

![Test Image 3](eval_loss.png)

![Test Image 4](learning_rate.png)

## QUESTIONS
1. **How long does it take to complete the training run? (hint: this session is on distributed training, so it will take a while)** <br>
It took 24 hours with 2 V100 GPU

2. Do you think your model is fully trained? How can you tell? <br>
![Test Image 1](eval_loss.png)

eval_loss is flattened, but BLUE score is still moving. so maybe approach to the end of training. 

3. Were you overfitting?
based on the graph..it does not look like it is overfitting

4. Were your GPUs fully utilized?

5. Did you monitor network traffic (hint: apt install nmon ) ? Was network the bottleneck?

6. Take a look at the plot of the learning rate and then check the config file. Can you explan this setting?
   The config file had the initial learning rate of 2.0 with "warmup_steps" of 8,000. If you observe the learning_rate graph, we can see the learning rate climb until the 8,000th step and start to decline afterwards.

7. How big was your training set (mb)? How many training lines did it contain?

8. What are the files that a TF checkpoint is comprised of?

9. How big is your resulting model checkpoint (mb)?

10. Remember the definition of a "step". How long did an average step take?
1.694s
11. How does that correlate with the observed network utilization between nodes?
The correlation between network speed and step duration is negative. The higher the network, the smaller the duration in seconds of the steps, as we can see from the previous point.
