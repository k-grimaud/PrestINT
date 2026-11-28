from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class Step(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)
    duration_days: int = Field(ge=0, le=365)
    assignee_id: UUID | None = None


class Template(BaseModel):
    steps: list[Step] = Field(max_length=20)

    @model_validator(mode="after")
    def unique_ids(self):
        """
        Making sure a template is described by a succession of steps without duplicate IDs
        """
        ids = [step.id for step in self.steps]

        if len(ids) != len(set(ids)):
            raise ValueError("step ids must be unique")

        return self
