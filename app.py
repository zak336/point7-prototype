import streamlit as st, json, time
from datetime import datetime
st.set_page_config(page_title="Point7 | No-Code AI Agent Builder",layout="wide")
st.markdown("""<style>.stApp{background:#f5f6fb}.hero{background:#1e2d62;color:white;padding:24px;border-radius:16px}.hero h1{color:white;margin:0}.hero p{color:#e0e6ff}.step{background:white;padding:14px;border:1px solid #dce1ef;border-radius:10px;margin-bottom:8px}</style>
<div class="hero"><h1>Point7</h1><p>No-Code AI Agent Builder · Describe a task. Review a workflow. Test the plan.</p><b>HACKATHON PROOF OF CONCEPT</b></div>""",unsafe_allow_html=True)
if "wf" not in st.session_state: st.session_state.wf=None
if "runs" not in st.session_state: st.session_state.runs=[]
st.write("")
a,b=st.columns([1.1,1])
with a:
 st.subheader("1. Describe a task")
 preset=st.selectbox("Example",["Custom task","Sort customer enquiries and draft replies","Research leads and prepare a summary","Analyse customer feedback","Turn meeting notes into action items"])
 examples={"Sort customer enquiries and draft replies":"Read customer enquiries, classify by topic and urgency, draft a reply, and create a follow-up list. Do not send messages automatically.","Research leads and prepare a summary":"Research potential business leads, summarise fit, and create a reviewable lead report.","Analyse customer feedback":"Group customer feedback into themes, flag urgent issues and produce a short summary.","Turn meeting notes into action items":"Extract decisions, owners, deadlines and follow-up tasks from meeting notes."}
 task=st.text_area("Natural-language instruction",examples.get(preset,""),height=130,placeholder="Describe the task, inputs, desired output and constraints.")
 risk=st.selectbox("Execution policy",["Review before action","Draft / analyse only","Low-risk steps only"])
 priority=st.selectbox("Optimisation priority",["Balanced","Lower cost","Higher quality","Lower latency"])
 make=st.button("Generate workflow",type="primary",use_container_width=True)
with b:
 st.subheader("2. Orchestration controls")
 st.info("This demo uses transparent rules to show the intended orchestration flow. No live model API or external tool is connected.")
 modelpref=st.selectbox("Model preference",["Auto-select (demo rules)","OpenAI-compatible API","Anthropic-compatible API","Local / open model"])
 tools=st.multiselect("Available tools",["Text/document input","Email draft (no sending)","Spreadsheet/CSV","Web research (simulated)","Task list (simulated)"],["Text/document input","Email draft (no sending)","Task list (simulated)"])
 maxsteps=st.slider("Maximum steps",3,6,5)
def build(t,p,r,m,tools,n):
 x=t.lower()
 if any(k in x for k in ["email","enquir","reply","support"]):
  typ="Customer communication"; model="General-purpose instruction-following model"; why="Requires text understanding, categorisation and controlled drafting."; toolplan=["Text/document input","Classification","Email draft (no sending)","Task list (simulated)"]
 elif any(k in x for k in ["lead","research","prospect","company"]):
  typ="Research and lead qualification"; model="Reasoning-capable model with research tools"; why="Requires information synthesis and consistent comparison."; toolplan=["Input list","Web research (simulated)","Lead scoring","Report output"]
 elif any(k in x for k in ["feedback","review","complaint","sentiment"]):
  typ="Feedback analysis"; model="Model with structured-output support"; why="Requires theme extraction, prioritisation and summarisation."; toolplan=["Text/document input","Theme classification","Priority detection","Summary output"]
 elif any(k in x for k in ["meeting","notes","action","deadline"]):
  typ="Document-to-actions"; model="Model with structured-output support"; why="Requires extraction into fields and checking missing details."; toolplan=["Notes input","Action-item extraction","Owner/deadline validation","Task list (simulated)"]
 else:
  typ="General task automation"; model="General-purpose instruction-following model"; why="Start with a capable model and validate structured output."; toolplan=["Task input","Plan generation","Output validation","Result summary"]
 if m!="Auto-select (demo rules)": model=m+" (preference selected; not API-tested)"
 routing={"Lower cost":"Prefer lower-cost models for routine steps; escalate if validation fails.","Higher quality":"Prefer stronger models for planning and validate outputs.","Lower latency":"Prefer fast models and keep the workflow short.","Balanced":"Balance capability, expected latency and estimated usage cost."}[p]
 steps=[("Understand request","Extract goal, inputs, constraints and expected output."),("Plan workflow","Convert the request into ordered steps with clear inputs/outputs."),("Select model and tools","Recommend components based on task type and priority."),("Execute bounded steps","Run only supported actions; gate external side effects."),("Validate result","Check required fields, missing data and obvious failures."),("Present result","Show output for review, approval or revision.")][:n]
 return {"created_at":datetime.now().isoformat(timespec="minutes"),"task":t,"task_type":typ,"model_recommendation":model,"reason":why,"routing_policy":routing,"tools":toolplan,"execution_policy":r,"steps":[{"step":i+1,"name":s,"details":d} for i,(s,d) in enumerate(steps)],"status":"Draft — not deployed","note":"Workflow generation, routing and test results are simulated in this prototype."}
if make:
 if task.strip(): st.session_state.wf=build(task,priority,risk,modelpref,tools,maxsteps)
 else: st.warning("Enter a task first.")
wf=st.session_state.wf
if wf:
 st.divider(); st.subheader("3. Generated workflow")
 c1,c2,c3=st.columns(3); c1.metric("Workflow type",wf["task_type"]); c2.metric("Planned steps",len(wf["steps"])); c3.metric("Deployment","Not enabled")
 st.markdown("**Task**"); st.write(wf["task"])
 x,y=st.columns([1.15,1])
 with x:
  st.markdown("#### Orchestration sequence")
  for q in wf["steps"]: st.markdown(f'<div class="step"><b>{q["step"]}. {q["name"]}</b><br>{q["details"]}</div>',unsafe_allow_html=True)
 with y:
  st.markdown("#### Model recommendation")
  st.success(wf["model_recommendation"]); st.write(wf["reason"])
  st.markdown("**Routing policy**"); st.write(wf["routing_policy"])
  st.markdown("**Planned tools**")
  for q in wf["tools"]: st.write("• "+q)
  st.markdown("**Safety policy**"); st.write(wf["execution_policy"])
 with st.expander("Inspect workflow JSON"): st.json(wf)
 d1,d2,d3=st.columns(3)
 with d1:
  test=st.button("Run simulated test",type="primary",use_container_width=True)
 with d2:
  st.download_button("Export workflow JSON",json.dumps(wf,indent=2),file_name="point7_workflow.json",mime="application/json",use_container_width=True)
 with d3:
  if st.button("Clear workflow",use_container_width=True): st.session_state.wf=None; st.rerun()
 if test:
  time.sleep(.4)
  checks=[("Task description present",bool(wf["task"].strip())),("At least three steps",len(wf["steps"])>=3),("Plan is reviewable",True),("External actions are not executed automatically",True)]
  st.subheader("4. Simulated test results")
  st.metric("Checks passed",f"{sum(v for _,v in checks)}/{len(checks)}")
  for name,ok in checks: st.success(name) if ok else st.error(name)
  st.caption("Simulated checks only: no live model API or external service was called.")
  st.session_state.runs.insert(0,{"time":datetime.now().strftime("%H:%M:%S"),"type":wf["task_type"],"passed":sum(v for _,v in checks)})
if st.session_state.runs:
 st.subheader("Recent simulated runs"); st.dataframe(st.session_state.runs,use_container_width=True)
with st.sidebar:
 st.title("Point7"); st.caption("Prototype status: early proof of concept")
 st.markdown("**Demonstrates**"); st.write("• Natural-language task intake\n• Model/tool recommendation logic\n• Workflow orchestration plan\n• Simulated test checks\n• JSON export")
 st.markdown("**Not implemented yet**"); st.write("• Live LLM calls\n• Real integrations\n• Real agent deployment\n• Production security/scaling")
