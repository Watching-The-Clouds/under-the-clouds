# Watching the clouds

## Weather-Based Delivery Analytics Platform  

This project is an end-to-end data engineering pipeline designed to provide insights on how weather conditions impact delivery times and associated costs. The solution is built on Python and AWS, integrating data ingestion, transformation, storage, and analytics to support delivery companies in optimizing their operations.  

## **Overview**  
Delivery companies face challenges when adverse weather conditions affect delivery schedules and costs. Our platform uses real-time and historical weather data to help these companies forecast delays, calculate additional costs such as fuel and driver overtime, and make informed decisions.  

### **Key Features:**  
- **Automated ETL Pipeline:** Retrieves data from the Weathermap API, processes it, and stores it in a queryable format.  
- **Scalable Design:** Uses AWS serverless technologies for cost efficiency and reliability.  
- **Custom Analytics API:** Delivers curated data insights for delivery companies.  
- **Data Storage:** Optimized PostgreSQL database on AWS Cloud for analytics and reporting.  

---

## **Architecture**  

1. **Data Ingestion:**  
   - A Lambda function fetches weather data from the Weathermap API.  
   - Stores raw JSON data in an S3 bucket.  

2. **Data Transformation:**  
   - A second Lambda function processes raw JSON data.  
   - Extracts relevant fields, normalizes data, and stores it in an S3 bucket for transformed data.  

3. **Data Storage:**  
   - Transformed data is loaded into a PostgreSQL database hosted on AWS RDS.  

4. **Analytics API:**  
   - A custom Python API serves insights, such as:  
     - Predicted delays based on weather conditions.  
     - Estimated cost increases for deliveries (fuel and overtime).  

5. **Orchestration and Logging:**  
   - Data flow is orchestrated programmatically between Lambda functions.  
   - CloudWatch logs provide monitoring and debugging.  

---

## **Technologies Used**  

- **Programming Language:** Python  
- **Cloud Services:**  
  - AWS Lambda (serverless compute)  
  - AWS S3 (data storage)  
  - AWS RDS (PostgreSQL database)  
  - CloudWatch (monitoring and logging)  
- **API Integration:** Weathermap API  

---

## **Getting Started**  

### **Prerequisites:**  
1. AWS account with necessary permissions for Lambda, S3, and RDS.  
2. Weathermap API key.  
3. Python 3.12 installed locally for development.  

### **Setup Instructions:**  
1. **Clone this repository:**  
   ```bash  
   git clone https://github.com/Watching-The-Clouds/under-the-clouds.git
   cd under-the-clouds  
   ```  
2. **Install dependencies:**  
   ```bash  
   make requirements
   ```  
3. **Deploy the AWS infrastructure:**  
   - Use the provided Terraform script.  
   - Configure environment variables in AWS Lambda for API keys and database credentials.  

4. **Run Locally (Optional):**  
   - Test the Lambda functions locally using the `serverless` framework or AWS SAM CLI.  

---

## **Usage**  

### **1. Ingest Weather Data**  
The first Lambda function runs at a scheduled interval, fetching data from the Weathermap API.  

### **2. Transform Data**  
The second Lambda function processes the raw JSON and stores the cleaned data in the transformed S3 bucket.  

### **3. Access Analytics**  
Use the custom API to query delivery insights, such as:  
   - Weather-induced delivery delays.  
   - Predicted cost adjustments based on weather forecasts.  

---

## **Contributing**  

Contributions are welcome! Please submit a pull request or open an issue to discuss proposed changes.