# dl-rerank (alpha)
Deep learning powered personalized re-ranking solution

#### User Interest Modeling Strategy
Given item list needed for ranking, we use DIN (deep interest network) modeling user diverse interest, DIEN is another good solution for this problem, the problem with this solution is we need to do lots of engineering optimization to get good performance when we use RNN, may be SRU is a candidate solution.

**Reference**
> [DIN](https://arxiv.org/abs/1706.06978): Deep Interest Network for Click-Through Rate Prediction <br />
> [DIEN](https://arxiv.org/abs/1809.03672): Deep Interest Evolution Network for Click-Through Rate Prediction <br />
> [SRU](https://arxiv.org/abs/1709.02755): Simple Recurrent Units for Highly Parallelizable Recurrence <br />

#### Item Modeling Strategy
After modeling user interest, given item targeted user vectorized representation and item list vectorized representation, and item click or not click label info. To precisely model (personalized user representation, item representation, context, label) relation, we need to consider item list info.

With item list info, we can compute each (personalized user representation, item representation)'s precise vectorized representation. Considering the computation budget we can apply dense tranformation before apply Transformer to do self-attention. We could use transformer to do user interest modeling also (BST).

Convolutional kernel give us another path to do self attention, we can finish this with Convolution, or Light Weight Convolution, or use Transformer and Light Convolution together which named by Long-Short Range Attention.

**Performance**<br />
hidden_size=256, kernel_size=3, batch_size=256, layer_num=3, filter_size=1024 <br />
hardware: (os) macos 10.13.4; (cpu) core i7 2.3 GHZ; (mem) 16GB <br />

| transformer   |      flatten transformer      |  lite transformer |  light conv    |
|---------------|:-----------------------------:|:-----------------:|:--------------:|
| 13.8ms/sample |         11.9ms/sample         |    11.5ms/sample  |  10ms/sample   |


**Reference**
>[Transformer](https://arxiv.org/abs/1706.03762): Attention Is All You Need <br />
>[PRM-Rerank](https://arxiv.org/abs/1904.06813): Personalized Re-ranking for Recommendation <br />
>[BST](https://arxiv.org/abs/1905.06874): Behavior Sequence Transformer for E-commerce Recommendation in Alibaba <br />
>[ConvSeq2Seq](https://arxiv.org/abs/1705.03122): Convolutional Sequence to Sequence Learning <br />
>[LightConv](https://arxiv.org/abs/1901.10430): Pay Less Attention with Light Weight and Dynamic Convolutions <br />
>[LSRA](https://arxiv.org/abs/2004.11886): Lite Transformer with Long-Short Range Attention <br />
>[GLU](https://arxiv.org/abs/2002.05202): GLU Variants Improve Transformer <br />

#### Multi-task learning
When developing a complicated machine learning application system, we need to consider multiple objectives, such as: click, dwell time, add basket, buy etc. Multi-task learning give us a solution to simultaneously learn multiple objectives.  <br />

There exists two type of multi-task learning: hard parameter sharing, soft parameter sharing. Here we use MMoE2, which is a soft parameter sharing method, and considering we use transformer to modeling inter-item relation, transformer is computation very costly, we use transformer as shared bottom layer, this architecture has also been tested by MT-DNN.  <br />


**Reference**
> [Survey](https://arxiv.org/abs/1706.05098): An Overview of Multi-Task Learning in Deep Neural Networks <br />
> [MMoE](https://dl.acm.org/doi/10.1145/3219819.3220007): Modeling task relationships in multi-task learning with multi-gate mixture-of-experts <br />
> [MMoE2](https://dl.acm.org/doi/10.1145/3298689.3346997): Recommending What Video to Watch Next: A Multitask Ranking System <br />
> [SNR](https://research.google/pubs/pub47842/): Sub-Network Routing for Flexible Parameter Sharing in Multi-Task Learning <br />
> [MT-DNN](https://arxiv.org/abs/1901.11504): Multi-Task Deep Neural Networks for Natural Language Understanding <br />


#### Engineering Related
> **Embedding**: support share embedding <br />
> **MBA**: support mini-batch aware regularization for sparse categorical feature <br />
> **XLA**: support xla <br />
> **Mixed Precision**: support mixed precision, **this feature can only be used with tf >=2.2.0** <br />
> **Distributed Training**: support parameter-server distributed training strategy <br />

### To do

**Position Bias Modeling** <br />
1) Recommending What Video to Watch Next: A Multitask Ranking System

**Ranking Position Modeling** <br />
1) Personalized Re-ranking for Recommendation

**Model Distillation** <br />
1) Ranking Distillation- Learning Compact Ranking Models With High Performance for Recommender System
