from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

@router.get("/socratic-prompts")
async def get_socratic_prompts() -> List[Dict[str, str]]:
    """Get Socratic learning prompts"""
    
    prompts = [
        {
            "question": "Why might crime rate affect housing prices more in some neighborhoods than others?",
            "context": "crime",
            "reflection": "Linear models assume constant effects, but social factors interact non-linearly."
        },
        {
            "question": "What social factors change with average number of rooms per dwelling?",
            "context": "rooms",
            "reflection": "Rooms correlate with wealth, family size, and neighborhood status."
        },
        {
            "question": "How would you explain the difference between Random Forest and Linear Regression to a peer?",
            "context": "models",
            "reflection": "One draws straight lines through data, the other learns complex patterns from examples."
        },
        {
            "question": "Why does education show diminishing returns on income in real data?",
            "context": "education",
            "reflection": "Human systems have ceilings and market saturation effects."
        },
        {
            "question": "What hidden variables might explain the relationship between rooms and housing price?",
            "context": "confounding",
            "reflection": "Correlation doesn't imply causation - wealth influences both."
        },
        {
            "question": "When would you trust Linear Regression over XGBoost?",
            "context": "model_selection",
            "reflection": "Simple, well-understood relationships with limited, clean data."
        }
    ]
    
    return prompts