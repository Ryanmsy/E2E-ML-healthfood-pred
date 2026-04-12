## Overview
End-to-end API food data pipeline based on OpenFoodFacts using Logistic Regression to predict if a food is healthy or not.

## Topics: 
API Ingestion
ETL Pipeline
Logistic Regression 
Random Forest
Inference
Model Monitoring

##  Understanding the Evaluation Metrics


### Macro Average
*Treats every class equally.*

* **Formula:** `(Metric Class 0 + Metric Class 1) / Total Number of Classes`
* **Intuition:** It penalizes the model evenly across all predictions . Because the model usually performs worse on a minority class (since it didn't have as much data or time to train on it), the Macro Average will drop heavily, making it easy to spot if the minority class is failing.

### Weighted Average
*Factors in the size of each class.*

* **Formula:** `(Metric Class 0 * (Count of Class 0 / Total Count)) + (Metric Class 1 * (Count of Class 1 / Total Count))`
* **Example:** `(0.85 * (292/426)) + (0.70 * (134/426))`
* **Intuition:** It is more "fair" for looking at overall performance because it scales the score based on how much weight each class actually holds in the dataset.


## 🚀 Model Deployment Strategy

When moving this project out of the development phase, there are two main architectural decisions to make: *how* the model serves predictions, and *where* it lives. 

### 1. How are we serving the model? (Online vs. Batch)

* **Online (Real-Time) Inference:** The model generates predictions instantly as new data arrives. 
  * *Example:* A self-driving vehicle processing new image frames every split second to determine its next movement. Latency and speed are the top priorities here.
  
* **Batch (Offline) Inference:** Predictions are generated on massive chunks of data all at once, typically on a set schedule (e.g., an overnight data pipeline). 
  * *The Advantage:* This allows us to maximize parallel processing. We can utilize GPUs to handle the heavy mathematical operations simultaneously, and use container orchestration tools (like Docker and Kubernetes) to break the massive workflow down into smaller, parallel computing jobs.

### 2. Where are we deploying it? (The Environment)

* **On-Premise:** Hosting on physical, in-house servers. We own the hardware and have total control over security, but we are responsible for all maintenance.

* **Cloud:** Utilizing managed providers (like AWS, Google Cloud, or Azure). This allows us to scale computing resources up or down easily based on the model's demand.

* **Edge:** Pushing the computation out to the "edge" of the network, closer to where the data is actually generated (like an IoT sensor or a smart camera). This reduces lag since the data doesn't have to travel all the way to a central cloud server.

* **On-Device (Local):** Running the model directly on an end-user's personal hardware, such as a laptop or smartphone. (This is exactly what we are doing when running the model locally during the development phase!)