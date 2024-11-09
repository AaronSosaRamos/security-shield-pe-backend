from pydantic import BaseModel, Field
from typing import List, Optional

class SecurityPlanInput(BaseModel):
    department: str
    province: str
    district: str
    mainTopic: str
    additionalDescription: str

class RiskIdentification(BaseModel):
    risk_id: str
    description: str = Field(..., description="Descripción detallada del riesgo identificado.")
    impact: str = Field(..., description="Impacto potencial del riesgo en la organización.")
    likelihood: int = Field(..., ge=1, le=5, description="Probabilidad de ocurrencia, del 1 (baja) al 5 (alta).")
    mitigation_measures: Optional[str] = Field(None, description="Medidas sugeridas para mitigar el riesgo.")

class SecurityRole(BaseModel):
    role_id: str
    title: str = Field(..., description="Título del rol de seguridad, como 'Administrador de Seguridad'.")
    responsibilities: str = Field(..., description="Descripción de las responsabilidades del rol.")
    contact_information: Optional[str] = Field(None, description="Información de contacto del responsable.")

class AssetProtection(BaseModel):
    asset_id: str
    asset_name: str = Field(..., description="Nombre del activo, como 'Servidor de Base de Datos'.")
    asset_type: str = Field(..., description="Tipo de activo, como 'Digital', 'Físico', etc.")
    protection_measures: str = Field(..., description="Medidas implementadas para proteger el activo.")
    potential_impact: str = Field(..., description="Impacto potencial de una brecha de seguridad en el activo.")

class IncidentResponseProcedure(BaseModel):
    procedure_id: str
    title: str = Field(..., description="Título del procedimiento de respuesta, como 'Respuesta a Incidentes de Phishing'.")
    steps: str = Field(..., description="Descripción paso a paso de las acciones a tomar durante el incidente.")
    responsible_roles: Optional[str] = Field(None, description="Roles responsables de ejecutar el procedimiento.")
    communication_plan: Optional[str] = Field(None, description="Plan de comunicación para notificar a los involucrados.")

class TrainingPlan(BaseModel):
    training_id: str
    topic: str = Field(..., description="Tema de la capacitación, como 'Buenas prácticas en seguridad informática'.")
    target_audience: str = Field(..., description="Grupo objetivo de la capacitación, como 'Todo el personal'.")
    schedule: str = Field(..., description="Fecha o frecuencia de la capacitación.")
    objectives: Optional[str] = Field(None, description="Objetivos de aprendizaje de la capacitación.")

class SecurityPolicy(BaseModel):
    policy_id: str
    title: str = Field(..., description="Título de la política, como 'Política de Control de Acceso'.")
    purpose: str = Field(..., description="Propósito de la política.")
    scope: str = Field(..., description="Alcance de la política, especificando a quiénes aplica.")
    enforcement: str = Field(..., description="Medidas para hacer cumplir la política.")
    review_date: Optional[str] = Field(None, description="Fecha de revisión de la política.")

class SecurityPlan(BaseModel):
    plan_id: str
    name: str = Field(..., description="Nombre del plan de seguridad, como 'Plan de Seguridad 2024'.")
    risk_identifications: List[RiskIdentification] = Field(..., description="Lista de riesgos identificados.")
    roles_and_responsibilities: List[SecurityRole] = Field(..., description="Roles de seguridad y sus responsabilidades.")
    assets: List[AssetProtection] = Field(..., description="Lista de activos y medidas de protección.")
    incident_response_procedures: List[IncidentResponseProcedure] = Field(..., description="Procedimientos de respuesta a incidentes.")
    training_plan: List[TrainingPlan] = Field(..., description="Plan de capacitación para el personal.")
    security_policies: List[SecurityPolicy] = Field(..., description="Políticas de seguridad de la organización.")
    creation_date: str = Field(..., description="Fecha de creación del plan.")
    revision_date: Optional[str] = Field(None, description="Fecha de revisión del plan de seguridad.")
