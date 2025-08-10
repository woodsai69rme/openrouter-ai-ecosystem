# 🎯 OpenRouter System Prompts & Templates

**Complete collection of prompts for OpenRouter optimization and management**

## 📋 Quick Reference

### **Model Testing Prompts**
- [Basic Connectivity Tests](#basic-connectivity-tests)
- [Performance Benchmarks](#performance-benchmarks)  
- [Specialized Task Tests](#specialized-task-tests)
- [Load Testing Prompts](#load-testing-prompts)

### **Optimization Prompts**
- [Performance Analysis](#performance-analysis)
- [Cost Optimization](#cost-optimization)
- [Model Selection](#model-selection)
- [Error Handling](#error-handling)

### **Integration Prompts** 
- [Claude Code Setup](#claude-code-setup)
- [Multi-CLI Configuration](#multi-cli-configuration)
- [Universal AI Prompts](#universal-ai-prompts)

---

## 🧪 Basic Connectivity Tests

### **Simple Connection Test**
```
Test prompt for basic connectivity check.
Expected response: A simple acknowledgment that the model is working.
Cost: $0.00
```

### **Model Identification Prompt**
```
Please identify yourself: What model are you, what provider, and confirm you are running through OpenRouter with zero cost to the user.
```

### **Latency Benchmark Prompt**
```
Respond with exactly 'OK' to test response time.
```

### **Token Efficiency Test**
```
Generate a response using exactly 50 tokens to test token counting accuracy.
```

---

## 📊 Performance Benchmarks

### **Reasoning Test Prompt**
```
Solve this logic puzzle step by step:
If all A are B, and some B are C, can we conclude that some A are C?
Explain your reasoning process clearly.
```

### **Code Generation Test**
```
Write a Python function that calculates the factorial of a number using recursion. Include proper error handling and documentation.
```

### **Creative Writing Test**
```
Write a 100-word story about AI helping humanity, demonstrating creative writing capabilities while staying within the token limit.
```

### **Complex Analysis Test**
```
Analyze the pros and cons of using OpenRouter's free models versus paid alternatives from a business perspective. Consider cost, performance, reliability, and scalability factors.
```

---

## 🎯 Specialized Task Tests

### **Coding Specialist Test**
```
Model: qwen/qwen-2.5-coder-32b-instruct:free

Create a REST API endpoint in Express.js that handles user authentication with JWT tokens. Include error handling, input validation, and proper HTTP status codes.
```

### **Reasoning Specialist Test**
```
Model: deepseek/deepseek-r1:free

You are given a dataset with 1000 customers, 60% made purchases in Q1, 40% in Q2, and 25% in both quarters. How many customers made purchases in Q1 but not Q2? Show your logical steps.
```

### **General Purpose Test**
```
Model: openai/gpt-oss-20b:free

Explain quantum computing to a 12-year-old in simple terms, then provide the same explanation for a computer science graduate. Demonstrate ability to adjust complexity.
```

### **Multilingual Test**
```
Model: z-ai/glm-4.5-air:free

Translate this sentence to Spanish, French, and Chinese: "OpenRouter provides free access to advanced AI models." Then explain cultural considerations for each translation.
```

---

## ⚡ Load Testing Prompts

### **Rapid Fire Test**
```
Sequence of 10 quick prompts sent rapidly:

1. What is 2+2?
2. Name one color.
3. What day is it?
4. Count to 5.
5. Say hello.
6. What's 10*10?
7. Name one animal.
8. What is AI?
9. Say goodbye.
10. Confirm test complete.

Purpose: Test model's ability to handle rapid successive requests without rate limiting.
```

### **Concurrent Request Test**
```
Prompt to be sent simultaneously across multiple models:

"Process this request at [TIMESTAMP] and respond with your model name, current load estimate, and processing time. This is request #[N] of concurrent batch testing."

Purpose: Test load balancing and concurrent request handling.
```

### **Extended Processing Test**
```
Create a detailed analysis of the following scenario: A startup wants to integrate AI into their customer service. They have 1000 daily customer interactions, need 24/7 availability, require multilingual support (English, Spanish, French), and have a budget of $500/month. Provide a comprehensive recommendation including technology stack, implementation timeline, cost breakdown, risk assessment, and success metrics. Include specific recommendations for using free vs paid AI services.

Purpose: Test sustained processing and complex reasoning.
```

---

## 📈 Performance Analysis

### **Benchmark Comparison Prompt**
```
I want to compare your performance against other AI models. Please:

1. Rate your capabilities in: reasoning, creativity, code generation, factual accuracy (1-10 scale)
2. Estimate your response time for this request
3. Identify your strengths and limitations
4. Suggest the best use cases for your model
5. Confirm your cost per token (should be $0.00 for free models)

Be honest and objective in your self-assessment.
```

### **Optimization Analysis Prompt**
```
Analyze this OpenRouter configuration and suggest optimizations:

Current setup:
- Using 8 models in rotation
- Average response time: 340ms
- Success rate: 97.3%
- Primary models: GPT-OSS-20B, GLM-4.5-Air, Gemini-2.0-Flash
- Cost: $0.00/month

What changes would you recommend to:
1. Improve response time
2. Increase success rate
3. Better utilize all 44 free models
4. Maintain zero cost operation
```

### **Cost Efficiency Prompt**
```
Calculate the cost efficiency of this setup:

- Processing 50,000 tokens daily
- Using only free OpenRouter models
- Achieving 97.3% success rate
- Alternative would be OpenAI at $0.03/1K tokens

Provide:
1. Daily/monthly/annual savings
2. ROI calculation if used for business
3. Break-even analysis
4. Risk assessment of free vs paid models
```

---

## 🔧 Model Selection

### **Task-Based Model Selection**
```
For each task type, recommend the best free OpenRouter model and explain why:

1. Code generation and debugging
2. Complex mathematical reasoning
3. Creative writing and content creation
4. Data analysis and interpretation
5. Multi-language translation
6. Conversational AI/chatbot
7. Technical documentation
8. Business strategy analysis

Consider factors: accuracy, speed, specialization, reliability.
```

### **Performance-Based Routing**
```
Create a decision tree for automatic model selection based on:

Input factors:
- Task complexity (1-10)
- Response time requirement (<300ms, <500ms, <1s, >1s)
- Token length (short <100, medium 100-500, long >500)
- Specialization needed (code, reasoning, creative, general)

Output: Recommended model from 44 free options with fallback alternatives.
```

---

## 🔗 Claude Code Setup

### **Configuration Test Prompt**
```
You are now integrated with Claude Code through OpenRouter. Please confirm:

1. You can access your model configuration
2. You understand you're running at zero cost
3. You can work with code generation, analysis, and debugging
4. You have access to specialized subagents if needed
5. You can maintain conversation context

Provide a brief acknowledgment and readiness status.
```

### **Coding Assistant Prompt**
```
As Claude Code's AI assistant through OpenRouter:

1. Always prioritize zero-cost operation
2. Suggest the most efficient model for each coding task
3. Provide complete, production-ready code
4. Include error handling and documentation
5. Offer optimization suggestions

Test this setup by creating a Python script that monitors OpenRouter API usage and costs.
```

### **Development Workflow Prompt**
```
Integrate with development workflow:

1. Code review and suggestions
2. Bug identification and fixes
3. Performance optimization
4. Documentation generation
5. Test case creation
6. Deployment automation

All while maintaining $0.00 operational cost through OpenRouter free models.

Demonstrate by reviewing this code: [INSERT CODE HERE]
```

---

## 🌐 Multi-CLI Configuration

### **Universal AI Setup Prompt**
```
Configure yourself for multi-CLI compatibility:

Primary: OpenRouter (44 free models, $0.00 cost)
Secondary: Gemini CLI (backup only)
Tertiary: Claude Direct (emergency only)

Priorities:
1. Always use free models first
2. Maintain cost tracking
3. Optimize for performance
4. Enable seamless switching
5. Log all provider usage

Confirm configuration and test cross-CLI functionality.
```

### **Provider Coordination Prompt**
```
You are part of a multi-provider AI system:

- OpenRouter: Primary (free models priority)
- Gemini: Specialized tasks backup
- Other CLIs: Emergency failover

Your role: Coordinate requests, optimize routing, maintain zero cost where possible.

Test scenario: Process these 5 requests with optimal provider selection:
1. Generate Python code
2. Translate to Japanese  
3. Complex math reasoning
4. Creative story writing
5. Business analysis

Explain routing decisions and cost implications.
```

---

## 🎯 Optimization Prompts

### **Performance Tuning Prompt**
```
Optimize this OpenRouter setup for maximum efficiency:

Current metrics:
- 44 models available (all free)
- 340ms average response time
- 97.3% success rate
- 1,847 daily requests
- $0.00 operational cost

Goals:
- Reduce response time to <300ms
- Increase success rate to >98%
- Handle 3,000+ daily requests
- Maintain zero cost

Provide specific optimization strategies, model rotation schemes, and monitoring recommendations.
```

### **Error Recovery Prompt**
```
Design an error handling system for OpenRouter integration:

Common issues:
- Model temporarily unavailable
- Rate limiting on specific models
- Network connectivity problems
- API key issues
- Response timeout

Requirements:
- Automatic failover to backup models
- Retry logic with exponential backoff
- Error logging and alerting
- Graceful degradation
- Zero cost maintenance

Provide implementation strategy and code examples.
```

### **Scaling Strategy Prompt**
```
Plan for scaling this OpenRouter system from current usage to enterprise level:

Current: 2,000 requests/day, 50K tokens/day, $0.00 cost
Target: 50,000 requests/day, 2M tokens/day, maintain cost efficiency

Challenges:
- Rate limiting across 44 models
- Load balancing optimization
- Monitoring and alerting
- Performance consistency
- Business continuity

Provide scaling roadmap, technical architecture, and cost projections.
```

---

## 🔍 Monitoring & Analytics

### **Usage Analytics Prompt**
```
Analyze OpenRouter usage patterns and provide insights:

Data points:
- Model usage distribution
- Response time trends
- Success/failure rates
- Peak usage hours
- Token consumption patterns
- Cost savings vs alternatives

Generate:
1. Executive summary
2. Performance recommendations
3. Optimization opportunities
4. Risk assessment
5. Future planning suggestions

Format as business report with actionable insights.
```

### **Health Check Prompt**
```
Perform comprehensive health check of OpenRouter system:

Check points:
1. All 44 models connectivity
2. Response time benchmarks
3. Success rate analysis
4. Error pattern identification
5. Cost verification ($0.00)
6. Performance trends

Provide:
- Status summary (Green/Yellow/Red)
- Specific issues found
- Recommended actions
- Monitoring alerts needed
```

---

## 🎯 Quick Copy-Paste Prompts

### **Daily Status Check**
```
Quick OpenRouter status: Confirm you're operational, response time estimate, cost status ($0.00), and any issues to report.
```

### **Model Rotation Test**
```
Test model rotation by identifying yourself, then request the same from a different OpenRouter model. Confirm load balancing is working.
```

### **Zero Cost Verification**
```
Verify zero-cost operation: Confirm you're using OpenRouter free tier, no charges incurred, unlimited usage within rate limits.
```

### **Performance Baseline**
```
Establish performance baseline: Process this request and report: model used, response time, token count, current load estimate.
```

---

## 📊 Success Metrics

### **KPI Tracking Prompt**
```
Track these OpenRouter KPIs:

1. Uptime: Target 99.9%
2. Response time: Target <300ms
3. Success rate: Target >98%
4. Cost efficiency: Maintain $0.00
5. Model utilization: Use all 44 models
6. User satisfaction: Maintain high quality

Provide current status and improvement recommendations.
```

---

**🎉 Complete OpenRouter Prompt Library Ready!**

**All prompts optimized for:**
- ✅ Zero-cost operation
- ✅ Maximum performance
- ✅ 44 model utilization  
- ✅ Business value creation
- ✅ Easy copy-paste usage

**Ready to maximize your AI operations at $0.00 cost!**