from openai import OpenAI

# Set your API key
openai_api_key = "ADD API KEY"

client = OpenAI(
    api_key=openai_api_key,  # This is the default and can be omitted
)

def generate_response(user_input):
    """
    Generates a response from OpenAI's GPT model using prompt engineering.
    """
    messages = [
        {"role": "system", "content": "You are an expert in optimizing geo-distributed LLM model serving. Provide efficient routing and model selection insights."},
        {"role": "user", "content": user_input}
    ]
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use "gpt-3.5-turbo" if needed (gpt-4o-mini)
        messages=messages,
        temperature=0.7,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.3
    )

    # Correct way to extract content
    return response.choices[0].message.content

# Example Usage
if __name__ == "__main__":

    user_query = """    
        I have a geo-distributed LLM model, partitioned across multiple nodes with specific roles. 
        Each node has different compute capabilities, and there is a need to minimize inference latency while balancing the load.

            Here are the metrics from Prometheus for the current load on each node:
            - US Node 1: Latency = 0.5s, Load = 60%, CPU Usage = 50%, Available GPUs = 2
            - Europe Node 1: Latency = 1.1s, Load = 75%, CPU Usage = 80%, Available GPUs = 1
            - Asia Node 1: Latency = 0.7s, Load = 65%, CPU Usage = 55%, Available GPUs = 2
            - US Node 2: Latency = 0.9s, Load = 80%, CPU Usage = 70%, Available GPUs = 1
            - Europe Node 2: Latency = 1.2s, Load = 70%, CPU Usage = 60%, Available GPUs = 1
                -Asia Node 2: Latency = 0.6s, Load = 85%, CPU Usage = 65%, Available GPUs = 2

            Additionally, we have the following model partitioning setup:
            - Partition 1 (Embedding Layer): US Node 1, Asia Node 2 and Europe Node 1
            - Partition 2 (Attention Layer): Asia Node 1 and US Node 2
            - Partition 3 (Output Layer): Europe Node 2 and Asia Node 1

        Please decide the optimal node selection for the first partition of the model, the subsequent partitions, and provide the most efficient routing strategy considering the metrics provided above."""
    
    ai_response = generate_response(user_query)
    print(ai_response)



# SAMPLE RESPONSE generated from above user_query
"""
Based on the provided metrics and model partitioning setup, we can optimize node selection for each partition and suggest an efficient routing strategy to minimize latency and balance 
the load across geo-distributed nodes.

### Optimal Node Selection for Model Partitions:

#### Partition 1 (Embedding Layer):
- Considering the available GPUs, CPU usage, and latency metrics:
  - US Node 1: Latency = 0.5s, Load = 60%, CPU Usage = 50%, Available GPUs = 2
  - Europe Node 1: Latency = 1.1s, Load = 75%, CPU Usage = 80%, Available GPUs = 1
  - Asia Node 2: Latency = 0.6s, Load = 85%, CPU Usage = 65%, Available GPUs = 2

#### Partition 2 (Attention Layer):
- Asia Node 1: Latency = 0.7s, Load = 65%, CPU Usage = 55%
- US Node 2: Latency = 0.9s, Load = 80%, CPU Usage = 70%

**Optimal Strategy**: Assign Partition 2 to Asia Node 1 and US Node 2 as they have relatively lower latency compared to other nodes.

#### Partition 3 (Output Layer):
- Europe Node 2: Latency = 1.2s, Load=70%, CPU Usage=60%
- Asia Node 1: Latency=0.7s, Load=65%, CPU Usage=55%

**Optimal Strategy**: Assign Partition 3 to Asia Node 1 as it has better latency performance compared to Europe Node 2.

### Efficient Routing Strategy:

To efficiently route requests through the optimized node selection for each partition:
- Route requests requiring the Embedding Layer to US Node 1 or Asia Node 2.
- Route requests requiring the Attention Layer to Asia Node 1 or US Node 2.
- Route requests requiring the Output Layer to Asia Node 1.

By following this routing strategy based on the optimal node selection for each partition, you can minimize latency and balance the load effectively across geo-distributed nodes in your LLM model serving infrastructure.r LLM model serving infrastructure.
"""