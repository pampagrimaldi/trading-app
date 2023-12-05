from trading_app import models
from sqlalchemy.orm import Session
from trading_app.database import SessionLocal
from tqdm import tqdm


strategy_list = ['opening_range_breakout','opening_range_breakdown']


def insert_strategies(session: Session, strategies: list):
	try:
		for strategy in tqdm(strategies):
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
		with SessionLocal() as session:
			insert_strategies(session, strategy_list)
	except Exception as e:
		print(f"Error during script execution: {e}")