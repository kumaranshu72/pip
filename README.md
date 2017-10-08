<h1>Introduction</h1>
This is a basic user based recommendation system based on collaborative filter using PIP as similarity measures.
<code>User Guide</code>
<ol>
   <li>Git Clone https://github.com/kumaranshu72/pip</li>
   <li>open rec.py and change the value of ID in estimate(ID,Similarity method) to get the prediction similar to the user.
   <li>open terminal and type python rec.py</li>
</ol>
  <code>You are done!!</coode>
<h1> Proximity Impact Popularity </h1>
<p>
 The core of collaborative filtering is to calculate similarities among users or items. The generic traditional similarity measures, such as Pearson correlation coefficient , cosine, mean squared difference, are not enough to capture the effective similar users, especially for cold user who only rates a small number of items.The new similarity model combines the local context for common ratings of each pair users and global preference of each user ratings. In order to test and verify the new similarity measure, experiments are implemented on three most used real data sets. In comparison with many state-of-the-art similarity measures, new model can show better recommended performance and better utilizes the ratings in cold user conditions.
</p>
<h1>The basic idea of the PIP similarity measure</h1>
<p>
The first factor, Proximity factor, not only calculates the absolute difference between two ratings, but also considers whether these ratings are in agreement or not, giving penalty to ratings in disagreement. </br>
The Impact factor represents how strongly an item is preferred or disliked by users.</br>
The last factor is Popularity. It denotes how common two user’s ratings have.
</p>
