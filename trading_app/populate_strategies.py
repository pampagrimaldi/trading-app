import os
from trading_app import models
from sqlalchemy.orm import Session
from trading_app.database import SessionLocal

strategy_dir = 'strategy'


def get_strategy_names(strategy_dir):
    try:
        # List all directories in the strategy folder
        strategy_names = [name for name in os.listdir(strategy_dir) if os.path.isdir(os.path.join(strategy_dir, name))]
        return strategy_names
    except Exception as e:
        print(f"Error fetching strategy names: {e}")
        return []


def insert_strategies(session: Session, strategies: list):
    try:
        for strategy in strategies:
            existing_strategy = session.query(models.Strategy).filter(models.Strategy.name == strategy).first()
            if not existing_strategy:
                print(f"Adding new strategy: {strategy}")
                new_strategy = models.Strategy(name=strategy)
                session.add(new_strategy)
            else:
                print(f"Strategy {strategy} already exists in the database.")
        session.commit()
    except Exception as e:
        print(f"Error during script execution: {e}")
        session.rollback()


if __name__ == "__main__":
    try:
        strategy_list = get_strategy_names(strategy_dir)
        with SessionLocal() as session:
            insert_strategies(session, strategy_list)
    except Exception as e:
        print(f"Error during script execution: {e}")
