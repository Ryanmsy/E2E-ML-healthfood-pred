## Overview
End-to-end API food data pipeline based on OpenFoodFacts using Logistic Regression to predict if a food is healthy or not.


Macro Avg = treats every class equally.

Metric Class x + Metric Class x + Metric Class x... / Total Num Class

 (metric 0 + metric 1 ) / 2 

 It penalizes everyone evenly but it would penalize mnoiire on the minoritry class because it will perform worse as it did not have the time to train hence it performed worst. 


 Weight Avg = 
 (Class x * No of Class x / Total Class) + (Class x * No of class x / Total Class)


(0.85 * (292/426)) + (0.70 * (134/426))

It is more fair be cause it penalize based on how much each weight the class is 



## how would we deploy it ? (Online / Batch) then Envinronments 

### First lets dicuss the difference of the 2 mains 

* Online = a model would use automatically at real time at every second. For example, self driving vehcile where every split second its a new image that the model would need to be applied and learn to make the next course of movement. 

* Batch = Do it overnight, or a huge chunks of data is batched into the model. Main great thing is GPU contains many processing units whih can run uin parallel -- I presume this is similiar to the concept of containers (dockers) and kubernets to ocerhates the huge workflow into smaller chunks running in parallel 


### Where would we we deploy it? (Environment)

* on premise  - using physical servers and managing them 

* Cloud - cloud providers like amazon, ibm 

* Edge - Combination of cloud on premise

* On device - personl devices laptop, smartphone (I guess this is what I am doing?)