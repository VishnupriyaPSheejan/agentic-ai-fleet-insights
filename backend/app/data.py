import os
SAMPLE = [
 dict(vehicle_id="VH-1001",customer_id="CUS-201",make="Ford",model="Escape",model_year=2018,mileage=112400,maintenance_cost=2450.0,days_since_service=190,risk_score=.86,replacement_candidate=True),
 dict(vehicle_id="VH-1002",customer_id="CUS-201",make="Ford",model="F-150",model_year=2021,mileage=64200,maintenance_cost=780.0,days_since_service=75,risk_score=.31,replacement_candidate=False),
 dict(vehicle_id="VH-1003",customer_id="CUS-202",make="Ford",model="Explorer",model_year=2017,mileage=128900,maintenance_cost=3120.0,days_since_service=240,risk_score=.93,replacement_candidate=True),
 dict(vehicle_id="VH-1004",customer_id="CUS-202",make="Ford",model="Transit",model_year=2020,mileage=88300,maintenance_cost=1670.0,days_since_service=150,risk_score=.67,replacement_candidate=False),
 dict(vehicle_id="VH-1005",customer_id="CUS-203",make="Ford",model="Mustang Mach-E",model_year=2023,mileage=28100,maintenance_cost=420.0,days_since_service=40,risk_score=.12,replacement_candidate=False),
 dict(vehicle_id="VH-1006",customer_id="CUS-204",make="Ford",model="Ranger",model_year=2019,mileage=104500,maintenance_cost=2210.0,days_since_service=210,risk_score=.81,replacement_candidate=True),
 dict(vehicle_id="VH-1007",customer_id="CUS-204",make="Ford",model="Transit",model_year=2022,mileage=51300,maintenance_cost=610.0,days_since_service=65,risk_score=.24,replacement_candidate=False),
 dict(vehicle_id="VH-1008",customer_id="CUS-205",make="Ford",model="Edge",model_year=2016,mileage=142700,maintenance_cost=3650.0,days_since_service=275,risk_score=.97,replacement_candidate=True),
 dict(vehicle_id="VH-1009",customer_id="CUS-206",make="Ford",model="Bronco Sport",model_year=2022,mileage=47300,maintenance_cost=530.0,days_since_service=58,risk_score=.22,replacement_candidate=False),
 dict(vehicle_id="VH-1010",customer_id="CUS-207",make="Ford",model="Super Duty",model_year=2019,mileage=119800,maintenance_cost=2890.0,days_since_service=225,risk_score=.88,replacement_candidate=True),
]
def get_vehicles():
    if os.getenv("DATA_SOURCE","demo").lower() != "bigquery":
        return [v.copy() for v in SAMPLE]
    from google.cloud import bigquery
    project, dataset = os.getenv("GCP_PROJECT_ID"), os.getenv("BIGQUERY_DATASET")
    table = os.getenv("BIGQUERY_VEHICLE_TABLE","fleet_vehicles")
    if not project or not dataset: raise ValueError("Set GCP_PROJECT_ID and BIGQUERY_DATASET.")
    client=bigquery.Client(project=project)
    sql=f"SELECT vehicle_id,customer_id,make,model,model_year,mileage,maintenance_cost,days_since_service,risk_score,replacement_candidate FROM `{project}.{dataset}.{table}` LIMIT 500"
    return [dict(r.items()) for r in client.query(sql).result()]
