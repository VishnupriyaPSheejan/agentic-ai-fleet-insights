from collections import defaultdict
import os
def run_workflow(question, vehicles):
    high=[v for v in vehicles if float(v["risk_score"])>=.75]
    candidates=[v for v in vehicles if v["replacement_candidate"]]
    groups=defaultdict(list)
    for v in vehicles: groups[v["customer_id"]].append(v)
    customers=sorted([{"customer_id":k,"vehicle_count":len(v),"average_risk":round(sum(float(x["risk_score"]) for x in v)/len(v),2)} for k,v in groups.items()],key=lambda x:x["average_risk"],reverse=True)
    overdue=sorted([v for v in vehicles if int(v["days_since_service"])>=150],key=lambda x:x["days_since_service"],reverse=True)
    total_cost=sum(float(v["maintenance_cost"]) for v in vehicles)
    agents=[
      {"agent":"Fleet Overview Agent","tool":"fleet_overview","result":f"Fleet contains {len(vehicles)} vehicles; {len(high)} are high risk and {len(candidates)} are replacement candidates.","metrics":{"total_vehicles":len(vehicles),"high_risk_vehicles":len(high),"replacement_candidates":len(candidates)}},
      {"agent":"Customer Insights Agent","tool":"customer_insights","result":"Customers ranked by average vehicle risk.","customers":customers[:5]},
      {"agent":"Vehicle Health Agent","tool":"vehicle_health","result":"Vehicles with the highest risk scores.","vehicles":[{"vehicle_id":v["vehicle_id"],"customer_id":v["customer_id"],"risk_score":v["risk_score"]} for v in sorted(vehicles,key=lambda x:x["risk_score"],reverse=True)[:5]]},
      {"agent":"Maintenance Agent","tool":"maintenance_analysis","result":f"{len(overdue)} vehicles have gone at least 150 days since service; total recorded maintenance cost is ${total_cost:,.0f}.","overdue_vehicles":[{"vehicle_id":v["vehicle_id"],"days_since_service":v["days_since_service"]} for v in overdue[:5]]},
      {"agent":"Replacement Opportunity Agent","tool":"replacement_opportunities","result":f"{len(candidates)} vehicles are flagged as replacement candidates.","candidates":[{"vehicle_id":v["vehicle_id"],"model":v["model"],"model_year":v["model_year"],"risk_score":v["risk_score"]} for v in sorted(candidates,key=lambda x:x["risk_score"],reverse=True)[:5]]},
      {"agent":"Recommendation Agent","tool":"recommendations","result":"Generated prioritized next steps.","recommendations":[f"Prioritize maintenance reviews for {len(high)} high-risk vehicles.",f"Schedule service follow-ups for {len(overdue)} overdue vehicles.",f"Review {len(candidates)} replacement candidates with customers."]},
    ]
    missing=[a["agent"] for a in agents if not a.get("result")]
    agents.append({"agent":"Critic Agent","tool":"quality_check","result":"Quality check passed." if not missing else "Review needed.","checks":{"agents_executed":len(agents),"missing_results":missing,"note":"Findings depend on the supplied data and are not a substitute for maintenance inspections."}})
    m=agents[0]["metrics"]
    return {"question":question,"title":"Fleet Insights Report","summary":f"Analyzed {m['total_vehicles']} vehicles. {m['high_risk_vehicles']} are high risk and {m['replacement_candidates']} are replacement candidates.","agent_count":len(agents),"agents":agents,"source":"BigQuery" if os.getenv("DATA_SOURCE","demo").lower()=="bigquery" else "Demo sample data"}
