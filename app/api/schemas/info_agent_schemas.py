from pydantic import BaseModel, Field, constr
from typing import List, Optional

class InfoAgentArgs(BaseModel):
    department: str
    province: str
    district: str
    description: str

class EmergencyContact(BaseModel):
    name: str = Field(..., description="Nombre del contacto de emergencia, como 'Policía', 'Bomberos', etc.")
    phone_number: str = Field(..., pattern=r"^\+?\d{9,15}$", description="Número de teléfono del contacto de emergencia.")
    description: Optional[str] = Field(None, description="Descripción del contacto, como su función específica o el tipo de emergencias que cubre.")

class AlarmActivation(BaseModel):
    location: str = Field(..., description="Ubicación o zona de cobertura del botón de activación de alarmas.")
    activation_code: Optional[str] = Field(None, description="Código de activación específico si existe.")
    response_time: Optional[int] = Field(None, description="Tiempo estimado de respuesta en minutos tras la activación.")
    active_status: bool = Field(..., description="Estado de activación actual del botón de alarmas.")

class NeighborhoodCommunication(BaseModel):
    platform: str = Field(..., description="Plataforma o medio de comunicación entre vecinos, como WhatsApp, Telegram, radio vecinal, etc.")
    contact_list: List[str] = Field(..., description="Lista de nombres o identificadores de vecinos en la plataforma.")
    description: Optional[str] = Field(None, description="Descripción del propósito o uso principal de la plataforma de comunicación.")

class KeyContacts(BaseModel):
    role: str = Field(..., description="Rol del contacto, como 'Serenazgo', 'Ambulancia', 'Familiar de Contacto', etc.")
    name: Optional[str] = Field(None, description="Nombre de la persona o institución de contacto.")
    phone_number: str = Field(..., pattern=r"^\+?\d{9,15}$", description="Número de teléfono del contacto clave.")
    available_hours: Optional[str] = Field(None, description="Horario de disponibilidad del contacto, si aplica.")

class HelpCenterLocation(BaseModel):
    center_name: str = Field(..., description="Nombre del centro de ayuda, como 'Hospital Central', 'Comisaría de distrito', etc.")
    address: str = Field(..., description="Dirección exacta del centro de ayuda.")
    contact_number: Optional[str] = Field(None, pattern=r"^\+?\d{9,15}$", description="Número de contacto del centro de ayuda.")
    services_provided: List[str] = Field(..., description="Servicios que ofrece el centro de ayuda, como 'atención médica', 'emergencias', 'seguridad', etc.")
    opening_hours: Optional[str] = Field(None, description="Horario de atención del centro de ayuda.")

class SecurityInformation(BaseModel):
    title: str = Field(..., description="Título o tipo de información de seguridad, como 'Consejos de prevención de robos'.")
    description: str = Field(..., description="Descripción detallada de la información en materia de seguridad.")
    last_updated: Optional[str] = Field(None, description="Fecha de la última actualización de la información de seguridad.")
    relevance: Optional[str] = Field(None, description="Relevancia o aplicabilidad de la información para la zona específica.")

class SecurityPlanDataCollection(BaseModel):
    department: str = Field(..., description="Departamento donde se realiza la recopilación de datos de seguridad.")
    province: str = Field(..., description="Provincia donde se realiza la recopilación de datos de seguridad.")
    district: str = Field(..., description="Distrito donde se realiza la recopilación de datos de seguridad.")
    emergency_contacts: List[EmergencyContact] = Field(..., description="Lista de contactos de emergencia disponibles.")
    alarm_activation_buttons: List[AlarmActivation] = Field(..., description="Lista de ubicaciones de botones de activación de alarmas y sus detalles.")
    neighborhood_communication_channels: List[NeighborhoodCommunication] = Field(..., description="Canales de comunicación entre vecinos.")
    key_contacts: List[KeyContacts] = Field(..., description="Lista de contactos clave de emergencia.")
    help_centers: List[HelpCenterLocation] = Field(..., description="Ubicación de centros de ayuda y servicios de emergencia.")
    security_information: List[SecurityInformation] = Field(..., description="Información relevante en materia de seguridad aplicable a la zona.")
