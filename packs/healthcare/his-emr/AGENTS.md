# AGENTS.md — HIS/EMR (L1)

L1 brief. At L2: separate the clinical record from the billing/insurance
record — clinical truth must never be edited to satisfy billing; model
clinical data on HL7 FHIR resources (Patient, Encounter, Observation,
MedicationRequest, …) with DICOM as the imaging boundary, not ad-hoc tables;
EMPI unmerge must be possible and audited; every amendment to a signed
clinical document is an addendum, never an in-place edit; ICD-10/11 and
terminology mapping is a versioned service; privacy (HIPAA-class and 等保2.0)
drives access control, audit trail, and retention stated per data class.
