def process_user_input(user_input):
    processed_input = {
        "description": f"Cliente em {user_input.location} com orçamento de R${user_input.budget:.2f} e necessidades de energia de {user_input.energy_needs}kWh/mês busca sistema de energia solar."
    }
    return processed_input
