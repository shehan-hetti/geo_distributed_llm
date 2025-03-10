# Geo-Distributed Large Language Model Serving and Fine-Tuning Platform

## Introduction

This project presents a geo-distributed large language model (LLM) serving and fine-tuning platform designed to address the limitations of traditional centralized AI-serving systems. By leveraging a network of geographically separated nodes, the platform improves scalability, fault tolerance, and performance.

## Problem Statement

Traditional AI-serving pipelines often rely on a single master or complex synchronization, typically hosted on central cloud platforms. These centralized systems can become bottlenecks and points of failure, leading to issues with scalability, latency, and reliability. Our project aims to build a distributed system that hosts a large language model (LLM) across multiple geographically separated nodes. Each node maintains a portion of the model’s parameters, ensuring inference across distributed nodes without conflict.

## Platform Design

The system design is structured to handle client requests efficiently across a geo-distributed network of nodes:
- **Client Request:** Sent to the Load Balancer via a REST API
- **Load Balancer:** Determines the optimal Inference Service Node based on geo-location and node availability.
- **Inference Service Node:** Pre-processes the request and sends it to the Inference Router via gRPC.
- **Inference Router:** Coordinates request processing by distributing tasks to LLM nodes based on the order of its layering, geo-location, and availability.
- **LLM Nodes:** Perform necessary computations on their portion of the model's parameters.
- **Inference Router (Response):** Gathers results from LLM nodes and sends the consolidated solution back to the Inference Service via gRPC.
- **Inference Service Node (Response):** Processes and structures the result for the client.
- **Database:** Maintains storage to manage prompt information for later fine-tuning stage.

## Implementation

The implementation involves various technologies and frameworks:
- **Programming Language:** Python
- **Software:**
  - **Docker:** Containerization of system components.
  - **Kubernetes:** Orchestration of Docker containers.
  - **Cassandra DB:** Distributed database.
- **Frameworks:**
  - **FastAPI:** For building the REST API.
  - **Python gRPC:** For communication between services.
  - **PyTorch:** For implementing the LLM.
- **Model:** Pre-trained models from the Hugging Face platform: GPT-2.

## Results

Quantitative results showcase the performance improvements achieved:
- **Latency:** Reduced response time compared to centralized systems.
- **Scalability:** Ability to handle increased client requests without performance degradation.
- **Fault Tolerance:** Resilience in handling node failures and maintaining availability.
- **Resource Utilization:** Efficient use of computational resources.

## Discussion

The project successfully demonstrates the potential of a geo-distributed LLM serving and fine-tuning platform. By addressing the limitations of traditional centralized AI-serving systems, it offers a robust solution for improved performance, scalability, and fault tolerance. The insights gained provide a solid foundation for future research and development in distributed machine learning.
