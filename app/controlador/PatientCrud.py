from connection import connect_to_mongodb
from bson import ObjectId
from fhir.resources.patient import Patient
import json

collection = connect_to_mongodb("SamplePatientService", "patients")

def GetPatientById(patient_id: str):
    try:
        patient = collection.find_one({"_id": ObjectId(patient_id)})
        if patient:
            patient["_id"] = str(patient["_id"])
            return "success", patient
        return "notFound", None
    except Exception as e:
        return f"notFound", None

def WritePatient(patient_dict: dict):
    try:
        pat = Patient.model_validate(patient_dict)
    except Exception as e:
        return f"errorValidating: {str(e)}",None
    validated_patient_json = pat.model_dump()
    result = collection.insert_one(patient_dict)
    if result:
        inserted_id = str(result.inserted_id)
        return "success",inserted_id
    else:
        return "errorInserting", None

def GetPatientByIdentifier(patientSystem, patientValue):
    try:
        print(f"🔍 Buscando en MongoDB con system={patientSystem}, value={patientValue}")  
        patient = collection.find_one({"identifier.system": patientSystem, "identifier.value": patientValue})  
        
        if patient:
            patient["_id"] = str(patient["_id"])
            print(f"✅ Paciente encontrado: {patient}")
            return "success", patient
        
        print("⚠️ Paciente no encontrado")
        return "notFound", None
    except Exception as e:
        print(f"❌ Error: {str(e)}")  # <-- Log del error exacto
        return f"error:{str(e)}", None