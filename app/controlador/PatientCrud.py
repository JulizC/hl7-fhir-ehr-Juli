from connection import connect_to_mongodb
from bson import ObjectId
from fhir.resources.patient import Patient  # ✅ Corrección aquí
import json

# Conexión a la base de datos y colección
collection = connect_to_mongodb("ifmerJuli", "patients")  # Cambia el nombre si usas otra BD

# Obtener paciente por ID
def GetPatientById(patient_id: str):
    try:
        patient = collection.find_one({"_id": ObjectId(patient_id)})
        if patient:
            patient["_id"] = str(patient["_id"])
            return "success", patient
        return "notFound", None
    except Exception as e:
        print(f"❌ Error en GetPatientById: {e}")
        return "notFound", None

# Insertar un nuevo paciente
def WritePatient(patient_dict: dict):
    try:
        pat = Patient.model_validate(patient_dict)  # ✅ Validación FHIR
    except Exception as e:
        print(f"❌ Error validando paciente: {e}")
        return f"errorValidating: {str(e)}", None

    validated_patient_json = pat.model_dump()
    try:
        result = collection.insert_one(validated_patient_json)
        return "success", str(result.inserted_id)
    except Exception as e:
        print(f"❌ Error insertando paciente: {e}")
        return "errorInserting", None

# Buscar paciente por identifier
def GetPatientByIdentifier(patientSystem, patientValue):
    try:
        print(f"🔍 Buscando en MongoDB con system={patientSystem}, value={patientValue}")
        patient = collection.find_one({
            "identifier": {
                "$elemMatch": {
                    "system": patientSystem,
                    "value": patientValue
                }
            }
        })
        if patient:
            patient["_id"] = str(patient["_id"])
            print(f"✅ Paciente encontrado: {patient}")
            return "success", patient
        
        print("⚠️ Paciente no encontrado")
        return "notFound", None
    except Exception as e:
        print(f"❌ Error en GetPatientByIdentifier: {e}")
        return f"error:{str(e)}", None
