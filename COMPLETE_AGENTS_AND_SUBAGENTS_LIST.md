# 🤖 COMPLETE AGENTS & SUBAGENTS INVENTORY
*Generated on: 2025-07-31*

## 📋 OVERVIEW

This comprehensive list covers all available agents and subagents across your system, including:
- **Claudia Built-in Agents** (3 Production-Ready)
- **Claude Code Subagents Collection** (45+ Specialized)
- **System-Available Subagents** (Built into Claude Code)
- **Third-Party Agent Libraries**

---

## 🎯 **CLAUDIA BUILT-IN AGENTS** (Production-Ready)

### 1. 🤖 **Git Commit Bot**
- **Model**: Sonnet
- **File**: `git-commit-bot.claudia.json`
- **Purpose**: Automated Git workflow management
- **Features**:
  - Analyzes git diff and status
  - Generates Conventional Commits messages
  - Handles merge conflicts intelligently
  - Automatic push to remote repositories
- **Default Task**: "Push all changes."
- **Status**: ✅ Ready to Use

### 2. 🛡️ **Security Scanner** 
- **Model**: Opus (Advanced)
- **File**: `security-scanner.claudia.json`
- **Purpose**: Static Application Security Testing (SAST)
- **Features**:
  - Multi-agent security audit system
  - Threat modeling (STRIDE methodology)
  - OWASP Top 10 vulnerability scanning
  - CWE (Common Weakness Enumeration) checks
  - Exploit validation and proof-of-concept
  - Professional security report generation
- **Default Task**: "Review the codebase for security issues."
- **Status**: ✅ Ready to Use

### 3. 🧪 **Unit Tests Bot**
- **Model**: Opus (Complex Analysis)
- **File**: `unit-tests-bot.claudia.json`
- **Purpose**: Automated comprehensive unit test generation
- **Features**:
  - Codebase structure analysis
  - Test plan generation
  - Style-matching test creation
  - Test execution verification
  - Coverage optimization (>80% overall, 100% critical paths)
  - Test documentation generation
- **Default Task**: "Generate unit tests for this codebase."
- **Status**: ✅ Ready to Use

---

## 🔧 **CLAUDE CODE SUBAGENTS COLLECTION** (45 Specialized)

### **🏗️ ARCHITECTURE & DESIGN (8 agents)**

#### 1. **backend-architect**
- **Purpose**: Design RESTful APIs, microservice boundaries, and database schemas
- **Specialties**: System architecture, scalability, performance bottlenecks
- **Use Cases**: Creating new backend services, API design

#### 2. **cloud-architect** 
- **Purpose**: Design AWS/Azure/GCP infrastructure, implement Terraform IaC
- **Specialties**: Auto-scaling, multi-region deployments, serverless architectures
- **Use Cases**: Cloud infrastructure, cost optimization, migration planning

#### 3. **api-documenter**
- **Purpose**: Create OpenAPI/Swagger specs, generate SDKs, write developer documentation
- **Specialties**: API documentation, versioning, examples, interactive docs
- **Use Cases**: API documentation, client library generation

#### 4. **graphql-architect**
- **Purpose**: Design GraphQL schemas, resolvers, and federation
- **Specialties**: Query optimization, N+1 problems, subscriptions
- **Use Cases**: GraphQL API design, performance issues

#### 5. **ui-ux-designer**
- **Purpose**: Create user interface designs and user experience flows
- **Specialties**: Wireframes, prototypes, accessibility, design systems
- **Use Cases**: UI/UX design, accessibility improvements

#### 6. **accessibility-specialist**
- **Purpose**: Ensure web accessibility compliance and inclusive design
- **Specialties**: WCAG guidelines, screen readers, keyboard navigation
- **Use Cases**: Accessibility audits, inclusive design implementation

#### 7. **performance-engineer**
- **Purpose**: Profile applications, optimize bottlenecks, implement caching strategies
- **Specialties**: Load testing, CDN setup, query optimization
- **Use Cases**: Performance issues, optimization tasks

#### 8. **legacy-modernizer**
- **Purpose**: Refactor legacy codebases, migrate outdated frameworks
- **Specialties**: Technical debt, dependency updates, backward compatibility
- **Use Cases**: Legacy system updates, framework migrations, technical debt reduction

### **💻 DEVELOPMENT & PROGRAMMING (12 agents)**

#### 9. **frontend-developer**
- **Purpose**: Build React components, implement responsive layouts, handle client-side state
- **Specialties**: Frontend performance, accessibility, UI components
- **Use Cases**: Creating UI components, fixing frontend issues

#### 10. **python-pro**
- **Purpose**: Write idiomatic Python code with advanced features
- **Specialties**: Decorators, generators, async/await, design patterns
- **Use Cases**: Python refactoring, optimization, complex Python features

#### 11. **javascript-pro**
- **Purpose**: Master modern JavaScript with ES6+, async patterns, Node.js APIs
- **Specialties**: Promises, event loops, browser/Node compatibility
- **Use Cases**: JavaScript optimization, async debugging, complex JS patterns

#### 12. **typescript-expert**
- **Purpose**: Advanced TypeScript development with complex type systems
- **Specialties**: Generics, mapped types, conditional types, type inference
- **Use Cases**: TypeScript refactoring, type system design

#### 13. **rust-pro**
- **Purpose**: Write idiomatic Rust with ownership patterns, lifetimes, trait implementations
- **Specialties**: Async/await, safe concurrency, zero-cost abstractions
- **Use Cases**: Rust memory safety, performance optimization, systems programming

#### 14. **golang-pro**
- **Purpose**: Write idiomatic Go code with goroutines, channels, and interfaces
- **Specialties**: Concurrency optimization, Go patterns, error handling
- **Use Cases**: Go refactoring, concurrency issues, performance optimization

#### 15. **cpp-pro**
- **Purpose**: Write idiomatic C++ code with modern features, RAII, smart pointers
- **Specialties**: Templates, move semantics, STL algorithms
- **Use Cases**: C++ refactoring, memory safety, complex C++ patterns

#### 16. **c-pro**
- **Purpose**: Write efficient C code with proper memory management, pointer arithmetic
- **Specialties**: Embedded systems, kernel modules, performance-critical code
- **Use Cases**: C optimization, memory issues, system programming

#### 17. **php-developer**
- **Purpose**: Modern PHP development with frameworks and best practices
- **Specialties**: Laravel, Symfony, PSR standards, security
- **Use Cases**: PHP application development, framework implementation

#### 18. **mobile-developer**
- **Purpose**: Develop React Native or Flutter apps with native integrations
- **Specialties**: Offline sync, push notifications, app store deployments
- **Use Cases**: Mobile features, cross-platform code, app optimization

#### 19. **game-developer**
- **Purpose**: Game development with various engines and frameworks
- **Specialties**: Unity, Unreal Engine, game mechanics, optimization
- **Use Cases**: Game development, performance optimization, game logic

#### 20. **nextjs-app-router-developer**
- **Purpose**: Next.js development with App Router and modern React patterns
- **Specialties**: Server components, streaming, middleware, SEO
- **Use Cases**: Next.js applications, SSR/SSG, performance optimization

### **🔍 TESTING & QUALITY (4 agents)**

#### 21. **test-automator**
- **Purpose**: Create comprehensive test suites with unit, integration, and e2e tests
- **Specialties**: CI pipelines, mocking strategies, test data
- **Use Cases**: Test coverage improvement, test automation setup

#### 22. **code-reviewer**
- **Purpose**: Expert code review for quality, security, and maintainability
- **Specialties**: Code quality, security vulnerabilities, best practices
- **Use Cases**: Code reviews, quality improvements

#### 23. **debugger**
- **Purpose**: Debug errors, test failures, and unexpected behavior
- **Specialties**: Error analysis, stack traces, debugging techniques
- **Use Cases**: Production issues, error investigation

#### 24. **security-auditor**
- **Purpose**: Review code for vulnerabilities, implement secure authentication
- **Specialties**: JWT, OAuth2, CORS, CSP, encryption, OWASP compliance
- **Use Cases**: Security reviews, auth flows, vulnerability fixes

### **🗄️ DATA & INFRASTRUCTURE (8 agents)**

#### 25. **data-engineer**
- **Purpose**: Build ETL pipelines, data warehouses, and streaming architectures
- **Specialties**: Spark jobs, Airflow DAGs, Kafka streams
- **Use Cases**: Data pipeline design, analytics infrastructure

#### 26. **data-scientist**
- **Purpose**: Data analysis expert for SQL queries, BigQuery operations, and insights
- **Specialties**: Statistical analysis, data visualization, machine learning
- **Use Cases**: Data analysis tasks, insights generation

#### 27. **database-optimizer**
- **Purpose**: Optimize SQL queries, design efficient indexes, handle database migrations
- **Specialties**: N+1 problems, slow queries, caching implementation
- **Use Cases**: Database performance issues, query optimization

#### 28. **database-admin**
- **Purpose**: Database administration, backup strategies, monitoring
- **Specialties**: PostgreSQL, MySQL, MongoDB administration
- **Use Cases**: Database maintenance, backup/restore, monitoring

#### 29. **sql-pro**
- **Purpose**: Advanced SQL query writing and database design
- **Specialties**: Complex joins, window functions, stored procedures
- **Use Cases**: Complex SQL queries, database schema design

#### 30. **ml-engineer**
- **Purpose**: Implement ML pipelines, model serving, and MLOps workflows
- **Specialties**: TensorFlow, PyTorch, model deployment, feature engineering
- **Use Cases**: ML model development, deployment, optimization

#### 31. **mlops-engineer**
- **Purpose**: ML operations, model monitoring, and automated retraining
- **Specialties**: MLflow, Kubeflow, model versioning, A/B testing
- **Use Cases**: ML pipeline automation, model monitoring

#### 32. **ai-engineer**
- **Purpose**: AI system design, LLM integration, and prompt engineering
- **Specialties**: OpenAI API, LangChain, vector databases, RAG systems
- **Use Cases**: AI feature development, LLM integration

### **🚀 DEVOPS & DEPLOYMENT (8 agents)**

#### 33. **devops-troubleshooter**
- **Purpose**: Debug production issues, analyze logs, and resolve infrastructure problems
- **Specialties**: Log analysis, monitoring, incident response
- **Use Cases**: Production debugging, incident resolution

#### 34. **deployment-engineer**
- **Purpose**: Set up CI/CD pipelines, automate deployments, manage environments
- **Specialties**: GitHub Actions, Jenkins, Docker, Kubernetes
- **Use Cases**: Deployment automation, CI/CD setup

#### 35. **terraform-specialist**
- **Purpose**: Infrastructure as Code with Terraform, manage cloud resources
- **Specialties**: AWS, Azure, GCP, state management, modules
- **Use Cases**: Infrastructure automation, cloud resource management

#### 36. **network-engineer**
- **Purpose**: Network configuration, security groups, load balancers
- **Specialties**: VPC design, DNS, CDN, network security
- **Use Cases**: Network setup, connectivity issues

#### 37. **directus-developer**
- **Purpose**: Directus CMS development and customization
- **Specialties**: Directus API, custom extensions, data modeling
- **Use Cases**: Directus implementation, custom features

#### 38. **docker-specialist**
- **Purpose**: Docker containerization and optimization
- **Specialties**: Multi-stage builds, image optimization, Docker Compose
- **Use Cases**: Containerization, Docker optimization

#### 39. **kubernetes-engineer**
- **Purpose**: Kubernetes cluster management and application deployment
- **Specialties**: Pod management, services, ingress, monitoring
- **Use Cases**: K8s deployment, cluster management

#### 40. **monitoring-specialist**
- **Purpose**: Application and infrastructure monitoring setup
- **Specialties**: Prometheus, Grafana, alerting, observability
- **Use Cases**: Monitoring setup, performance tracking

### **💰 FINANCE & CRYPTO (5 agents)**

#### 41. **crypto-trader**
- **Purpose**: Cryptocurrency trading strategies and market analysis
- **Specialties**: Technical analysis, trading bots, risk management
- **Use Cases**: Trading strategy development, market analysis

#### 42. **crypto-analyst**
- **Purpose**: Blockchain analysis and cryptocurrency research
- **Specialties**: On-chain analysis, tokenomics, project evaluation
- **Use Cases**: Crypto research, investment analysis

#### 43. **crypto-risk-manager**
- **Purpose**: Risk assessment and portfolio management for crypto investments
- **Specialties**: Risk modeling, portfolio optimization, compliance
- **Use Cases**: Risk management, portfolio analysis

#### 44. **defi-strategist**
- **Purpose**: DeFi protocol analysis and yield farming strategies
- **Specialties**: Liquidity mining, protocol analysis, smart contracts
- **Use Cases**: DeFi strategy, yield optimization

#### 45. **quant-analyst**
- **Purpose**: Quantitative analysis and algorithmic trading
- **Specialties**: Statistical modeling, backtesting, algorithm development
- **Use Cases**: Quantitative strategies, algorithm development

### **🛠️ SPECIALIZED TOOLS (5 agents)**

#### 46. **payment-integration**
- **Purpose**: Payment gateway integration and financial transactions
- **Specialties**: Stripe, PayPal, cryptocurrency payments, compliance
- **Use Cases**: Payment system integration, transaction handling

#### 47. **blockchain-developer**
- **Purpose**: Smart contract development and blockchain integration
- **Specialties**: Solidity, Web3, DApp development, testing
- **Use Cases**: Smart contract development, blockchain integration

#### 48. **arbitrage-bot**
- **Purpose**: Automated arbitrage trading across exchanges
- **Specialties**: Price monitoring, automated trading, risk management
- **Use Cases**: Arbitrage opportunities, automated trading

#### 49. **api-integrator**
- **Purpose**: Third-party API integration and data synchronization
- **Specialties**: REST APIs, GraphQL, webhooks, rate limiting
- **Use Cases**: API integration, data synchronization

#### 50. **automation-specialist**
- **Purpose**: Process automation and workflow optimization
- **Specialties**: Zapier, workflow automation, business process optimization
- **Use Cases**: Process automation, workflow optimization

---

## 🎯 **RECOMMENDED AGENT WORKFLOWS**

### **Development Workflow**
1. **backend-architect** - Design system architecture
2. **frontend-developer** - Implement UI components
3. **code-reviewer** - Review code quality
4. **test-automator** - Generate comprehensive tests
5. **security-auditor** - Security review
6. **deployment-engineer** - Deploy to production

### **Data Pipeline Workflow**
1. **data-engineer** - Design ETL pipeline
2. **database-optimizer** - Optimize queries
3. **ml-engineer** - Implement ML models
4. **mlops-engineer** - Set up monitoring
5. **devops-troubleshooter** - Production support

### **Crypto Trading Workflow**
1. **crypto-analyst** - Market research
2. **quant-analyst** - Strategy development
3. **crypto-trader** - Execute trades
4. **crypto-risk-manager** - Risk assessment
5. **arbitrage-bot** - Automated opportunities

---

## 🚀 **QUICK START GUIDE**

### **Using Agents in Your Workflow**

1. **Identify Your Task**: Determine which category your task falls into
2. **Select Appropriate Agent**: Choose the most specialized agent for your needs
3. **Provide Context**: Give clear, specific instructions
4. **Review Output**: Validate the agent's work
5. **Iterate**: Refine and improve based on results

### **Best Practices**

- **Be Specific**: Provide detailed requirements and context
- **Use Multiple Agents**: Combine agents for complex workflows
- **Validate Output**: Always review and test agent-generated code
- **Provide Feedback**: Help agents learn and improve
- **Document Results**: Keep track of successful patterns

---

## 📚 **ADDITIONAL RESOURCES**

- **Agent Configuration Files**: Located in project directories
- **Custom Agent Creation**: Use existing agents as templates
- **Integration Guides**: Framework-specific implementation guides
- **Performance Metrics**: Agent effectiveness tracking
- **Community Contributions**: Shared agent configurations

---

*This inventory is continuously updated as new agents are developed and existing ones are enhanced.*