"""
Contract Analysis Multi-Agent System - Core Components
"""

import os
import json
import PyPDF2
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

from agno.agent import Agent
from agno.models.mistral import MistralChat
from agno.team.team import Team
from agno.tools.reasoning import ReasoningTools
from agno.tools.file import FileTools
import os


@dataclass
class AgentResponse:
    """Structured response from individual agents"""
    agent_name: str
    timestamp: str
    analysis_type: str
    findings: Dict
    recommendations: List[str]
    risk_level: str
    confidence_score: float


@dataclass
class ContractAnalysisResult:
    """Complete analysis result with full traceability"""
    contract_info: Dict
    agent_responses: List[AgentResponse]
    consolidated_findings: Dict
    priority_recommendations: List[str]
    risk_assessment: Dict
    traceability_map: Dict[str, str]
    analysis_timestamp: str


class ContractAnalysisSystem:
    """Multi-Agent Contract Analysis System with complete traceability"""
    
    def __init__(self):
        """Initialize the multi-agent system"""
        self.agents = {}
        self.manager_agent = None
        self.analysis_history = []
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all specialized agents"""
        try:
            # Import your AI framework here (e.g., from crewai import Agent)
            # This is a placeholder - replace with your actual agent initialization
            
            # Structure Agent
            self.agents["structure"] = self._create_structure_agent()
            
            # Legal Agent
            self.agents["legal"] = self._create_legal_agent()
            
            # Negotiation Agent
            self.agents["negotiation"] = self._create_negotiation_agent()
            
            # Manager Agent
            self.manager_agent = self._create_manager_agent()
            
        except Exception as e:
            raise Exception(f"Failed to initialize agents: {e}")
    
    def _create_structure_agent(self):
        """Create the Contract Structure Analysis Agent"""
        structure_agent = Agent(
            name="ContractStructureAgent",
            role="Contract Structure & Organization Specialist",
            model=MistralChat(id="open-mistral-nemo"),
            instructions=[
                "You are a CONTRACT STRUCTURE SPECIALIST. Your role is to analyze and organize contract components systematically.",
                "",
                "🎯 PRIMARY OBJECTIVES:",
                "• Identify and categorize all contract parties and their defined roles",
                "• Map out main terms, conditions, and mutual obligations",
                "• Analyze payment structures, amounts, schedules, and conditions",
                "• Extract deliverables, milestones, and performance metrics",
                "• Examine duration, renewal options, and termination conditions",
                "• Assess risk allocation and responsibility distribution",
                "",
                "📋 STRUCTURAL ANALYSIS CHECKLIST:",
                "• Contract header and identification information",
                "• Party definitions and legal entity details", 
                "• Scope of work and service descriptions",
                "• Timeline and milestone definitions",
                "• Financial terms and payment mechanics",
                "• Performance standards and acceptance criteria",
                "• Change management and modification procedures",
                "• Termination triggers and procedures",
                "",
                "🚨 RED FLAGS TO IDENTIFY:",
                "• Missing essential contract elements",
                "• Ambiguous or contradictory terms",
                "• Unbalanced obligation distribution",
                "• Vague performance standards",
                "• Incomplete termination procedures",
                "• Missing change management processes",
                "",
                "📊 OUTPUT REQUIREMENTS:",
                "• Provide structured analysis using clear categories",
                "• Rate completeness on scale 1-10 with justification",
                "• List specific gaps or improvements needed",
                "• Assign risk level: LOW/MEDIUM/HIGH for structural issues",
                "• Include confidence score (0.0-1.0) for your analysis",
                "",
                "Format your response as structured JSON with these sections:",
                "- contract_parties",
                "- main_terms", 
                "- payment_structure",
                "- deliverables_timeline",
                "- termination_conditions",
                "- structural_gaps",
                "- completeness_score",
                "- risk_level",
                "- recommendations"
            ],
            markdown=True
        )
        return structure_agent

    def _create_legal_agent(self):
        """Create the Legal Framework Analysis Agent"""
        legal_agent = Agent(
            name="LegalFrameworkAgent", 
            role="Legal Compliance & Risk Assessment Specialist",
            model=MistralChat(id="open-mistral-nemo"),
            instructions=[
                "You are a LEGAL COMPLIANCE SPECIALIST. Your role is to assess legal validity, compliance, and risk exposure.",
                "",
                "⚖️ LEGAL ANALYSIS FOCUS:",
                "• Enforceability of contract terms under applicable law",
                "• Jurisdiction and governing law appropriateness",
                "• Liability allocation and limitation clause effectiveness", 
                "• Indemnification provisions and mutual protection",
                "• Intellectual property rights and ownership clarity",
                "• Confidentiality and non-disclosure adequacy",
                "• Dispute resolution mechanisms and enforceability",
                "• Regulatory compliance requirements",
                "",
                "🔍 COMPLIANCE CHECKLIST:",
                "• Contract formation requirements (offer, acceptance, consideration)",
                "• Capacity and authority of signing parties",
                "• Statutory and regulatory compliance",
                "• Industry-specific legal requirements",
                "• Consumer protection law considerations",
                "• Employment law implications (if applicable)",
                "• Data protection and privacy compliance",
                "",
                "⚠️ LEGAL RISK ASSESSMENT:",
                "• HIGH RISK: Unenforceable terms, regulatory violations, excessive liability",
                "• MEDIUM RISK: Ambiguous clauses, jurisdiction issues, incomplete protection",
                "• LOW RISK: Minor technical issues, formatting problems",
                "",
                "🛡️ RISK MITIGATION PRIORITIES:",
                "• Identify unenforceable or problematic clauses",
                "• Recommend liability protection improvements",
                "• Suggest regulatory compliance enhancements",
                "• Propose dispute resolution optimization",
                "",
                "📋 OUTPUT REQUIREMENTS:",
                "• Categorize findings by legal area (contract law, regulatory, IP, etc.)",
                "• Assign risk levels with specific justification",
                "• Provide actionable legal recommendations",
                "• Include confidence score for legal assessment",
                "",
                "Format response as structured JSON with sections:",
                "- enforceability_assessment",
                "- compliance_review", 
                "- liability_analysis",
                "- risk_factors",
                "- legal_gaps",
                "- regulatory_issues",
                "- risk_level",
                "- recommendations"
            ],
            markdown=True
        )
        return legal_agent

    def _create_negotiation_agent(self):
        """Create the Negotiation Strategy Agent"""
        negotiation_agent = Agent(
            name="NegotiationAgent",
            role="Strategic Negotiation & Business Optimization Specialist", 
            model=MistralChat(id="open-mistral-nemo"),
            instructions=[
                "You are a STRATEGIC NEGOTIATION SPECIALIST. Your role is to optimize contract terms through strategic negotiation analysis.",
                "",
                "🎯 NEGOTIATION STRATEGY FOCUS:",
                "• Power dynamics and leverage analysis between parties",
                "• Win-win opportunity identification and value creation",
                "• Alternative terms and creative solution development",
                "• Market benchmarking and industry standard comparison",
                "• Risk-reward balance optimization",
                "• Relationship preservation considerations",
                "",
                "💪 LEVERAGE ASSESSMENT:",
                "• Client leverage factors (market position, alternatives, urgency)",
                "• Counterparty leverage factors (competition, capacity, dependency)",
                "• Mutual dependencies and shared interests",
                "• External market factors and timing considerations",
                "",
                "🎲 NEGOTIATION TACTICS:",
                "• Priority terms ranking (must-have vs. nice-to-have)",
                "• Trade-off opportunities and package deals",
                "• Timing and sequencing strategies",
                "• Fallback positions and walkaway points",
                "• Escalation and decision-making processes",
                "",
                "📈 VALUE OPTIMIZATION:",
                "• Cost reduction opportunities",
                "• Revenue enhancement possibilities", 
                "• Risk mitigation through better terms",
                "• Operational efficiency improvements",
                "• Long-term relationship value",
                "",
                "🗣️ COMMUNICATION STRATEGY:",
                "• Key messaging and positioning",
                "• Stakeholder alignment requirements",
                "• Documentation and follow-up needs",
                "• Relationship management considerations",
                "",
                "📊 OUTPUT REQUIREMENTS:",
                "• Prioritize negotiation points by business impact",
                "• Provide specific tactical recommendations",
                "• Include alternative term suggestions",
                "• Assess negotiation difficulty and timeline",
                "",
                "Format response as structured JSON with sections:",
                "- leverage_analysis",
                "- priority_terms",
                "- negotiation_tactics",
                "- alternative_terms",
                "- value_optimization",
                "- implementation_strategy",
                "- risk_level", 
                "- recommendations"
            ],
            markdown=True
        )
        return negotiation_agent

    def _create_manager_agent(self):
        """Create the Manager Consolidation Agent"""
        manager_agent = Team(
            name="ContractAnalysisManager",
            mode="coordinate",
            model=MistralChat(id="open-mistral-nemo"),
            members=[
            self.agents["structure"],
            self.agents["legal"],
            self.agents["negotiation"]
        ],
            tools=[ReasoningTools(add_instructions=True), FileTools()],
            instructions=[
                 "You are the Contract Analysis Team Manager. Execute analysis in this sequence:",
        "",
        "ANALYSIS WORKFLOW:",
        "1. STRUCTURE ANALYSIS: Have the Structure Agent analyze the contract organization and completeness",
        "2. LEGAL REVIEW: Have the Legal Agent assess compliance and legal risks", 
        "3. NEGOTIATION STRATEGY: Have the Negotiation Agent develop strategic recommendations",
        "4. SYNTHESIS: Integrate all findings into a comprehensive report",
        "",
        "FINAL OUTPUT REQUIREMENTS:",
        "• Executive Summary (2-3 key points per category)",
        "• Structural Assessment with gaps identified",
        "• Legal Risk Analysis with prioritized recommendations",
        "• Negotiation Strategy with specific tactics",
        "• Implementation Roadmap with next steps",
        "",
        "QUALITY STANDARDS:",
        "• Be specific and actionable",
        "• Prioritize by business impact",
        "• Provide clear rationale for recommendations",
        "• Focus on practical implementation",
        "",
        "IMPORTANT: Complete the analysis efficiently without task loops or redundant coordination."
            ],
            markdown=True
        )

        return manager_agent


def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
    """
    Extract text content from PDF file with comprehensive error handling
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text content or None if failed
    """
    try:
        if not os.path.exists(pdf_path):
            print(f"❌ Error: File '{pdf_path}' does not exist")
            return None
            
        if not os.access(pdf_path, os.R_OK):
            print(f"❌ Error: No read permission for file '{pdf_path}'")
            return None
            
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            if len(pdf_reader.pages) == 0:
                print("❌ Error: PDF file appears to be empty")
                return None
                
            text_content = []
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text.strip():
                        text_content.append(f"--- Page {page_num + 1} ---")
                        text_content.append(page_text)
                except Exception as page_error:
                    print(f"⚠️  Warning: Could not extract text from page {page_num + 1}: {page_error}")
                    continue
                    
            if not text_content:
                print("❌ Warning: No readable text found in PDF")
                return None
                
            return "\n".join(text_content)
            
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return None


def analyze_contract(system: ContractAnalysisSystem, contract_text: str, contract_name: str = "Contract") -> ContractAnalysisResult:
    """
    Execute complete contract analysis using the multi-agent system
    
    Args:
        system: ContractAnalysisSystem instance
        contract_text: Text content of the contract
        contract_name: Name/identifier for the contract
        
    Returns:
        ContractAnalysisResult: Complete analysis with traceability
    """
    
    print(f"\n{'='*80}")
    print(f"🏢 CONTRACT ANALYSIS: {contract_name}")
    print(f"{'='*80}")
    print(f"📄 Contract Length: {len(contract_text):,} characters")
    print(f"⏰ Analysis Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}")
    
    agent_responses = []
    
    # Step 1: Structure Agent Analysis
    print("\n🏗️  PHASE 1: STRUCTURAL ANALYSIS")
    print("-" * 40)
    
    structure_prompt = f"""
    Analyze this contract's structure and organization.
    
    CONTRACT TO ANALYZE:
    {contract_text}
    
    Focus on completeness, organization, and structural integrity.
    """
    
    try:
        print("📋 Structure Agent analyzing...")
        structure_response = system.agents["structure"].run(structure_prompt)
        
        structure_analysis = AgentResponse(
            agent_name="ContractStructureAgent",
            timestamp=datetime.now().isoformat(),
            analysis_type="structural_analysis",
            findings={"raw_response": structure_response.content if hasattr(structure_response, 'content') else str(structure_response)},
            recommendations=[],
            risk_level="PENDING",
            confidence_score=0.8
        )
        agent_responses.append(structure_analysis)
        print("✅ Structure analysis completed")
        
    except Exception as e:
        print(f"❌ Structure Agent error: {e}")
        structure_analysis = AgentResponse(
            agent_name="ContractStructureAgent",
            timestamp=datetime.now().isoformat(), 
            analysis_type="structural_analysis",
            findings={"error": str(e)},
            recommendations=["Manual structure review required"],
            risk_level="HIGH",
            confidence_score=0.3
        )
        agent_responses.append(structure_analysis)
    
    # Step 2: Legal Agent Analysis  
    print("\n⚖️  PHASE 2: LEGAL COMPLIANCE ANALYSIS")
    print("-" * 40)
    
    legal_prompt = f"""
    Conduct legal compliance and risk assessment for this contract. Provide analysis in JSON format.
    
    CONTRACT TO ANALYZE:
    {contract_text}
    
    Focus on enforceability, compliance, and legal risk factors.
    """
    
    try:
        print("🏛️  Legal Agent analyzing...")
        legal_response = system.agents["legal"].run(legal_prompt)
        
        legal_analysis = AgentResponse(
            agent_name="LegalFrameworkAgent",
            timestamp=datetime.now().isoformat(),
            analysis_type="legal_compliance",
            findings={"raw_response": legal_response.content if hasattr(legal_response, 'content') else str(legal_response)},
            recommendations=[],
            risk_level="PENDING", 
            confidence_score=0.85
        )
        agent_responses.append(legal_analysis)
        print("✅ Legal analysis completed")
        
    except Exception as e:
        print(f"❌ Legal Agent error: {e}")
        legal_analysis = AgentResponse(
            agent_name="LegalFrameworkAgent",
            timestamp=datetime.now().isoformat(),
            analysis_type="legal_compliance", 
            findings={"error": str(e)},
            recommendations=["Legal review by qualified attorney required"],
            risk_level="HIGH",
            confidence_score=0.2
        )
        agent_responses.append(legal_analysis)
    
    # Step 3: Negotiation Agent Analysis
    print("\n🤝 PHASE 3: NEGOTIATION STRATEGY ANALYSIS") 
    print("-" * 40)
    
    negotiation_prompt = f"""
    Develop negotiation strategy and optimization recommendations for this contract. Provide analysis in JSON format.
    
    CONTRACT TO ANALYZE:
    {contract_text}
    
    Focus on leverage, optimization opportunities, and strategic recommendations.
    """
    
    try:
        print("💼 Negotiation Agent analyzing...")
        negotiation_response = system.agents["negotiation"].run(negotiation_prompt)
        
        negotiation_analysis = AgentResponse(
            agent_name="NegotiationAgent", 
            timestamp=datetime.now().isoformat(),
            analysis_type="negotiation_strategy",
            findings={"raw_response": negotiation_response.content if hasattr(negotiation_response, 'content') else str(negotiation_response)},
            recommendations=[],
            risk_level="PENDING",
            confidence_score=0.75
        )
        agent_responses.append(negotiation_analysis)
        print("✅ Negotiation analysis completed")
        
    except Exception as e:
        print(f"❌ Negotiation Agent error: {e}")
        negotiation_analysis = AgentResponse(
            agent_name="NegotiationAgent",
            timestamp=datetime.now().isoformat(),
            analysis_type="negotiation_strategy",
            findings={"error": str(e)},
            recommendations=["Manual negotiation strategy development required"],
            risk_level="MEDIUM", 
            confidence_score=0.4
        )
        agent_responses.append(negotiation_analysis)
    
    # Step 4: Manager Consolidation
    print("\n🎯 PHASE 4: MANAGEMENT CONSOLIDATION & TRACEABILITY")
    print("-" * 40)
    
    consolidation_prompt = f"""
    CONSOLIDATE AND SYNTHESIZE the following agent analyses with FULL TRACEABILITY:

    CONTRACT NAME: {contract_name}
    
    STRUCTURE AGENT FINDINGS:
    {structure_analysis.findings}
    
    LEGAL AGENT FINDINGS: 
    {legal_analysis.findings}
    
    NEGOTIATION AGENT FINDINGS:
    {negotiation_analysis.findings}
    
    Your task as Manager is to:
    1. Synthesize these 3 perspectives into unified insights
    2. Maintain complete traceability to source agents
    3. Resolve conflicts between agent recommendations  
    4. Prioritize actions by business impact and risk
    5. Create implementation roadmap
    
    CRITICAL: Every recommendation must cite which agent(s) contributed to it.
    """
    
    try:
        print("👨‍💼 Manager Agent consolidating...")
        manager_response = system.manager_agent.run(consolidation_prompt)
        print("✅ Management consolidation completed")
        
        # Create final analysis result
        analysis_result = ContractAnalysisResult(
            contract_info={
                "name": contract_name,
                "length": len(contract_text),
                "analysis_date": datetime.now().isoformat()
            },
            agent_responses=agent_responses,
            consolidated_findings={
                "manager_synthesis": manager_response.content if hasattr(manager_response, 'content') else str(manager_response)
            },
            priority_recommendations=[],
            risk_assessment={},
            traceability_map={
                "structure_agent": "ContractStructureAgent", 
                "legal_agent": "LegalFrameworkAgent",
                "negotiation_agent": "NegotiationAgent",
                "manager_agent": "ContractAnalysisManager"
            },
            analysis_timestamp=datetime.now().isoformat()
        )
        
        return analysis_result
        
    except Exception as e:
        print(f"❌ Manager Agent error: {e}")
        
        # Return partial results even if manager fails
        analysis_result = ContractAnalysisResult(
            contract_info={
                "name": contract_name,
                "length": len(contract_text), 
                "analysis_date": datetime.now().isoformat()
            },
            agent_responses=agent_responses,
            consolidated_findings={"error": f"Manager consolidation failed: {e}"},
            priority_recommendations=["Manual review and consolidation required"],
            risk_assessment={"overall_risk": "UNKNOWN - Analysis incomplete"},
            traceability_map={
                "structure_agent": "ContractStructureAgent",
                "legal_agent": "LegalFrameworkAgent", 
                "negotiation_agent": "NegotiationAgent",
                "manager_agent": "ContractAnalysisManager (FAILED)"
            },
            analysis_timestamp=datetime.now().isoformat()
        )
        
        return analysis_result


def display_analysis_results(result: ContractAnalysisResult):
    """Display comprehensive analysis results with traceability"""
    
    print(f"\n{'🎯 FINAL ANALYSIS RESULTS':=^80}")
    print(f"\n📋 CONTRACT: {result.contract_info['name']}")
    print(f"📅 ANALYZED: {result.contract_info['analysis_date']}")
    print(f"📄 LENGTH: {result.contract_info['length']:,} characters")
    
    print(f"\n{'AGENT TRACEABILITY MAP':^80}")
    print("=" * 80)
    for role, agent_name in result.traceability_map.items():
        status = "✅ COMPLETED" if not any("error" in resp.findings or "FAILED" in agent_name for resp in result.agent_responses if resp.agent_name == agent_name) else "❌ FAILED"
        print(f"{role.replace('_', ' ').title():.<40} {agent_name} {status}")
    
    print(f"\n{'INDIVIDUAL AGENT RESPONSES':^80}")
    print("=" * 80)
    
    for i, response in enumerate(result.agent_responses, 1):
        print(f"\n{i}. {response.agent_name} ({response.analysis_type})")
        print(f"   Timestamp: {response.timestamp}")
        print(f"   Risk Level: {response.risk_level}")
        print(f"   Confidence: {response.confidence_score:.1%}")
        print(f"   Findings Preview: {str(response.findings)[:200]}...")
        if response.recommendations:
            print(f"   Key Recommendations: {', '.join(response.recommendations[:3])}")
    
    print(f"\n{'MANAGER CONSOLIDATED ANALYSIS':^80}")
    print("=" * 80)
    
    if "error" not in result.consolidated_findings:
        print(result.consolidated_findings.get("manager_synthesis", "No synthesis available"))
    else:
        print(f"❌ CONSOLIDATION ERROR: {result.consolidated_findings['error']}")
        print("\n📋 INDIVIDUAL AGENT SUMMARIES:")
        for response in result.agent_responses:
            print(f"\n🤖 {response.agent_name}:")
            if "error" not in response.findings:
                findings_text = str(response.findings.get('raw_response', ''))
                print(f"   {findings_text[:300]}..." if len(findings_text) > 300 else findings_text)
            else:
                print(f"   ❌ {response.findings['error']}")
    
    print(f"\n{'ANALYSIS COMPLETE':=^80}")


def save_analysis_results(result: ContractAnalysisResult, output_dir: str = "analysis_results"):
    """Save analysis results to JSON file for future reference"""
    
    try:
        # Create output directory
        Path(output_dir).mkdir(exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        contract_name_clean = "".join(c for c in result.contract_info['name'] if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = f"contract_analysis_{contract_name_clean}_{timestamp}.json"
        filepath = Path(output_dir) / filename
        
        # Convert to JSON-serializable format
        result_dict = asdict(result)
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Analysis results saved to: {filepath}")
        return str(filepath)
        
    except Exception as e:
        print(f"❌ Error saving analysis results: {e}")
        return None