# Sentinel Design Document

## 1. Overview

Sentinel is an intelligent AI Gateway that sits between an application and one or more Large Language Model (LLM) providers. Instead of an application communicating directly with a specific provider such as Groq or OpenAI, every request is first sent to Sentinel. The gateway is responsible for routing requests to the appropriate provider while handling common infrastructure concerns such as caching, rate limiting, provider failover, and future observability integration.

The goal of Sentinel is to provide a single, reliable entry point for all AI requests, making AI-powered applications more resilient, cost-efficient, and easier to manage.

---

## 2. Problem Statement

Modern AI applications often communicate directly with a single LLM provider. While this approach is simple, it introduces several challenges:

- The application becomes dependent on one provider.
- If the provider experiences downtime, the application cannot serve requests.
- Identical prompts result in repeated API calls, increasing latency and unnecessary costs.
- Excessive or malicious requests can rapidly consume API quotas and increase expenses.
- Infrastructure logic such as retries, routing, and provider management becomes duplicated across multiple applications.

A centralized AI Gateway addresses these challenges by handling them in one place instead of requiring every application to implement the same functionality independently.

---

## 3. Proposed Solution

Sentinel acts as a centralized gateway between client applications and multiple LLM providers.

The request flow is:

Application
→ Sentinel AI Gateway
→ Selected LLM Provider
→ Response returned to the application

Before forwarding a request to a provider, Sentinel performs several checks and decisions, including:

- Validating that the client has not exceeded its rate limit.
- Checking whether an identical request already exists in the cache.
- Selecting the most appropriate provider based on routing rules.
- Falling back to an alternative provider if the primary provider is unavailable.

By centralizing these responsibilities, applications remain simple while Sentinel manages reliability, performance, and cost optimization.

---

## 4. Supported Providers

### Primary Provider - Groq

Groq will serve as the default provider for the Minimum Viable Product (MVP). It offers a generous free tier, low latency, and is well suited for rapid experimentation and development.

### Fallback Provider - OpenAI

OpenAI will be configured as the secondary provider. If the primary provider becomes unavailable or a request cannot be completed successfully, Sentinel will automatically retry the request using OpenAI.

### Stretch Goal - Ollama

As a future enhancement, Sentinel will support Ollama for locally hosted language models. This enables offline inference, eliminates API costs for supported models, and provides an additional routing option.

---

## 5. Minimum Viable Product (MVP)

The MVP of Sentinel will be considered complete when it supports the following functionality:

- FastAPI-based HTTP service.
- A `/chat` endpoint for accepting prompt requests.
- Routing requests to the Groq API.
- Automatic fallback to OpenAI when Groq is unavailable.
- Exact prompt-response caching.
- Token Bucket rate limiting.
- Basic circuit breaker for provider failures.
- Configuration through environment variables.
- Basic logging for incoming requests and provider responses.

---

## 6. Future Enhancements

Future versions of Sentinel may include:

- Semantic caching using embeddings.
- Intelligent provider selection based on latency, cost, or model capability.
- Support for additional LLM providers.
- Request queuing and retry mechanisms.
- Monitoring dashboards and metrics.
- Integration with Vigil for end-to-end AI observability and failure analysis.

---

## 7. Success Criteria

Sentinel will be considered successful when an application can communicate with multiple LLM providers through a single API endpoint while benefiting from caching, rate limiting, provider failover, and centralized request management without requiring changes to application code.