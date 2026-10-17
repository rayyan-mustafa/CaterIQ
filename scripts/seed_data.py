"""Seed script populating realistic catering demo data for CaterIQ.

Creates:
- Demo Organization: 'Apex Artisan Catering'
- Users: 'demo@cateriq.com' (Owner, pass: 'Password123!'), 'chef@cateriq.com' (Manager)
- Locations: 'Central Commissary Kitchen', 'Downtown Event Hub'
- Allergen catalog & linked ingredients
- Graph of ingredient substitutions for BFS allergen search
- Dishes across Starters, Mains, Desserts, and Drinks
- Sample packages
- CRM Clients with event history
- Events in various lifecycle stages (Lead, Proposed, Confirmed, Completed)
- Proposals, Invoices, and Payments
"""

from datetime import date, datetime, timedelta, timezone
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session
from backend.app.core.database import Base, SessionLocal, engine
from backend.app.core.security import hash_password
from backend.app.models.organization import Location, Membership, Organization
from backend.app.models.user import User
from backend.app.models.client import Client
from backend.app.models.menu import (
    Allergen,
    Ingredient,
    IngredientAllergen,
    IngredientSubstitution,
    MenuItem,
    MenuItemIngredient,
    Package,
    PackageItem,
)
from backend.app.models.event import Event, EventItem
from backend.app.models.billing import Invoice, Payment, Proposal
from backend.app.models.support import CalendarToken, TravelTime


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def seed():
    print("[INIT] Initializing database schema...")
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # Check if already seeded
        existing_user = db.query(User).filter(User.email == "demo@cateriq.com").first()
        if existing_user:
            print("[INFO] Demo account already exists. Skipping seed.")
            return

        print("[ACCOUNTS] Creating organization and demo accounts...")
        org = Organization(name="Apex Artisan Catering")
        db.add(org)
        db.flush()

        # Users
        owner = User(
            email="demo@cateriq.com",
            password_hash=hash_password("Password123!"),
            full_name="Rayyan Mustafa",
            is_active=True,
        )
        manager = User(
            email="chef@cateriq.com",
            password_hash=hash_password("Password123!"),
            full_name="Elena Rostova",
            is_active=True,
        )
        db.add_all([owner, manager])
        db.flush()

        # Locations
        loc1 = Location(
            organization_id=org.id,
            name="Central Commissary Kitchen",
            address="142 Industrial Blvd, Suite 4",
            latitude=40.7128,
            longitude=-74.0060,
        )
        loc2 = Location(
            organization_id=org.id,
            name="Downtown Event Hub",
            address="500 Broadway St",
            latitude=40.7282,
            longitude=-73.9942,
        )
        db.add_all([loc1, loc2])
        db.flush()

        # Memberships
        m1 = Membership(user_id=owner.id, organization_id=org.id, role="owner")
        m2 = Membership(user_id=manager.id, organization_id=org.id, role="manager", location_id=loc1.id)
        db.add_all([m1, m2])

        # Calendar Token
        cal_tok = CalendarToken(organization_id=org.id, token="demo-calendar-token-apex-2026")
        db.add(cal_tok)

        print("[ALLERGENS] Seeding allergens, ingredients, and substitutions...")
        allergens = {
            "peanut": Allergen(name="peanut"),
            "tree_nut": Allergen(name="tree_nut"),
            "gluten": Allergen(name="gluten"),
            "dairy": Allergen(name="dairy"),
            "soy": Allergen(name="soy"),
            "shellfish": Allergen(name="shellfish"),
            "egg": Allergen(name="egg"),
        }
        for a in allergens.values():
            db.add(a)
        db.flush()

        # Ingredients
        def make_ing(name, unit, cost, *alg_keys):
            ing = Ingredient(organization_id=org.id, name=name, unit=unit, cost_per_unit=cost)
            db.add(ing)
            db.flush()
            for k in alg_keys:
                db.add(IngredientAllergen(ingredient_id=ing.id, allergen_id=allergens[k].id))
            return ing

        peanut_butter = make_ing("Peanut Butter", "kg", 4.50, "peanut")
        sunflower_butter = make_ing("Sunflower Seed Butter", "kg", 6.00)
        almond_butter = make_ing("Almond Butter", "kg", 8.50, "tree_nut")
        wheat_flour = make_ing("Wheat Flour", "kg", 1.20, "gluten")
        rice_flour = make_ing("Rice Flour", "kg", 2.00)
        heavy_cream = make_ing("Heavy Cream", "liter", 3.80, "dairy")
        coconut_cream = make_ing("Coconut Cream", "liter", 4.20)
        chicken_breast = make_ing("Chicken Breast", "kg", 7.50)
        ribeye_steak = make_ing("Ribeye Beef", "kg", 18.00)
        wild_salmon = make_ing("Wild Salmon", "kg", 16.00)
        arborio_rice = make_ing("Arborio Rice", "kg", 3.00)
        parmesan_cheese = make_ing("Parmesan Cheese", "kg", 14.00, "dairy")
        vegan_parmesan = make_ing("Nutritional Yeast Seasoning", "kg", 9.00)
        olive_oil = make_ing("Extra Virgin Olive Oil", "liter", 9.50)
        eggs = make_ing("Fresh Farm Eggs", "dozen", 3.50, "egg")
        apples = make_ing("Honeycrisp Apples", "kg", 2.80)

        # Allowed Substitutions (Graph for BFS)
        substitutions = [
            (peanut_butter, sunflower_butter, 1.0, "Safe nut-free alternative"),
            (peanut_butter, almond_butter, 1.0, "Tree-nut alternative"),
            (almond_butter, sunflower_butter, 1.0, "Eliminate tree-nut"),
            (wheat_flour, rice_flour, 1.0, "Gluten-free flour replacement"),
            (heavy_cream, coconut_cream, 1.0, "Dairy-free creamy texture"),
            (parmesan_cheese, vegan_parmesan, 1.0, "Vegan dairy-free savory topping"),
        ]
        for f, t, cost, note in substitutions:
            db.add(IngredientSubstitution(
                organization_id=org.id,
                from_ingredient_id=f.id,
                to_ingredient_id=t.id,
                swap_cost=cost,
                notes=note,
            ))

        print("[MENU] Seeding menu items...")
        dishes = [
            # Starters
            MenuItem(
                organization_id=org.id,
                name="Tuscan Bruschetta on Sourdough",
                category="starter",
                description="Heirloom tomatoes, fresh basil, and balsamic reduction.",
                price_per_head=9.00,
                cost_per_head=2.50,
                is_vegetarian=True,
                is_vegan=True,
                is_gluten_free=False,
                popularity_score=0.92,
            ),
            MenuItem(
                organization_id=org.id,
                name="Gluten-Free Caprese Skewers",
                category="starter",
                description="Cherry tomatoes, buffalo mozzarella, and pesto drizzle.",
                price_per_head=11.00,
                cost_per_head=3.20,
                is_vegetarian=True,
                is_vegan=False,
                is_gluten_free=True,
                popularity_score=0.88,
            ),
            MenuItem(
                organization_id=org.id,
                name="Thai Satay Skewers",
                category="starter",
                description="Grilled chicken skewers with signature peanut dipping sauce.",
                price_per_head=12.50,
                cost_per_head=3.80,
                is_vegetarian=False,
                is_gluten_free=False,
                popularity_score=0.95,
            ),
            # Mains
            MenuItem(
                organization_id=org.id,
                name="Wild Truffle Mushroom Risotto",
                category="main",
                description="Creamy arborio rice with foraged mushrooms and aged parmesan.",
                price_per_head=24.00,
                cost_per_head=6.50,
                is_vegetarian=True,
                is_vegan=False,
                is_gluten_free=True,
                popularity_score=0.94,
            ),
            MenuItem(
                organization_id=org.id,
                name="Pan-Seared Atlantic Salmon",
                category="main",
                description="Crispy skin salmon with lemon-dill glaze and asparagus.",
                price_per_head=29.00,
                cost_per_head=9.00,
                is_vegetarian=False,
                is_vegan=False,
                is_gluten_free=True,
                popularity_score=0.91,
            ),
            MenuItem(
                organization_id=org.id,
                name="Prime Angus Ribeye Medallions",
                category="main",
                description="Herb butter, roasted garlic potato purée, red wine jus.",
                price_per_head=36.00,
                cost_per_head=12.50,
                is_vegetarian=False,
                is_vegan=False,
                is_gluten_free=True,
                popularity_score=0.97,
            ),
            MenuItem(
                organization_id=org.id,
                name="Roasted Cauliflower Steak",
                category="main",
                description="Chimichurri sauce, quinoa pilaf, and pomegranate jewels.",
                price_per_head=22.00,
                cost_per_head=4.80,
                is_vegetarian=True,
                is_vegan=True,
                is_gluten_free=True,
                popularity_score=0.82,
            ),
            # Desserts
            MenuItem(
                organization_id=org.id,
                name="Classic Madagascar Vanilla Panna Cotta",
                category="dessert",
                description="Berry compote and fresh mint.",
                price_per_head=8.50,
                cost_per_head=2.10,
                is_vegetarian=True,
                is_gluten_free=True,
                popularity_score=0.89,
            ),
            MenuItem(
                organization_id=org.id,
                name="Dark Chocolate Lava Cake",
                category="dessert",
                description="Warm molten chocolate center with salted caramel.",
                price_per_head=9.50,
                cost_per_head=2.70,
                is_vegetarian=True,
                is_gluten_free=False,
                popularity_score=0.96,
            ),
            MenuItem(
                organization_id=org.id,
                name="Seasonal Berry Sorbet Trio",
                category="dessert",
                description="Raspberry, mango, and passionfruit refreshing sorbet.",
                price_per_head=7.50,
                cost_per_head=1.80,
                is_vegetarian=True,
                is_vegan=True,
                is_gluten_free=True,
                popularity_score=0.85,
            ),
            # Drinks
            MenuItem(
                organization_id=org.id,
                name="Artisanal Cold-Pressed Juices",
                category="drink",
                description="Orange ginger and green detox blends.",
                price_per_head=6.00,
                cost_per_head=1.50,
                is_vegetarian=True,
                is_vegan=True,
                is_gluten_free=True,
                popularity_score=0.87,
            ),
            MenuItem(
                organization_id=org.id,
                name="Sparkling Botanical Mocktails",
                category="drink",
                description="Lavender lemonade and cucumber elderflower spritz.",
                price_per_head=7.00,
                cost_per_head=1.70,
                is_vegetarian=True,
                is_vegan=True,
                is_gluten_free=True,
                popularity_score=0.91,
            ),
        ]
        for d in dishes:
            db.add(d)
        db.flush()

        # Link Satay to Peanut Butter ingredient
        satay_dish = next(d for d in dishes if "Satay" in d.name)
        db.add(MenuItemIngredient(menu_item_id=satay_dish.id, ingredient_id=peanut_butter.id, quantity=1.0))
        db.add(MenuItemIngredient(menu_item_id=satay_dish.id, ingredient_id=chicken_breast.id, quantity=1.0))

        # Link Bruschetta to Wheat Flour
        bruschetta_dish = next(d for d in dishes if "Bruschetta" in d.name)
        db.add(MenuItemIngredient(menu_item_id=bruschetta_dish.id, ingredient_id=wheat_flour.id, quantity=1.0))

        print("[CLIENTS] Seeding CRM clients...")
        c1 = Client(
            organization_id=org.id,
            name="Sarah Jenkins",
            email="sarah.jenkins@techcorp.io",
            phone="+1 (555) 234-5678",
            company_name="TechCorp Global",
            notes="Prefers organic sourcing; annual holiday gala client.",
        )
        c2 = Client(
            organization_id=org.id,
            name="Marcus Vance",
            email="m.vance@vanceholdings.com",
            phone="+1 (555) 876-5432",
            company_name="Vance Financial Group",
            notes="High VIP expectations, executive board dinners.",
        )
        c3 = Client(
            organization_id=org.id,
            name="Emily & Daniel Thorne",
            email="emily.thorne@gmail.com",
            phone="+1 (555) 432-1098",
            company_name="Private Client",
            notes="Autumn outdoor wedding, 140 guests.",
        )
        db.add_all([c1, c2, c3])
        db.flush()

        print("[EVENTS] Seeding events, proposals, invoices, and payments...")
        today = date.today()

        # Event 1: Completed Event (Past Month)
        ev1 = Event(
            organization_id=org.id,
            location_id=loc1.id,
            client_id=c1.id,
            title="TechCorp Q3 Leadership Summit",
            event_date=today - timedelta(days=20),
            start_time="11:30",
            end_time="15:30",
            venue_address="TechCorp Campus, Bldg B",
            headcount=85,
            status="completed",
            notes="Flawless execution; requested same menu for Q4.",
        )
        db.add(ev1)
        db.flush()

        # Attach items to ev1
        m_bruschetta = dishes[0]
        m_salmon = dishes[4]
        m_pannacotta = dishes[7]
        db.add_all([
            EventItem(event_id=ev1.id, menu_item_id=m_bruschetta.id, quantity=1, unit_price=m_bruschetta.price_per_head, unit_cost=m_bruschetta.cost_per_head),
            EventItem(event_id=ev1.id, menu_item_id=m_salmon.id, quantity=1, unit_price=m_salmon.price_per_head, unit_cost=m_salmon.cost_per_head),
            EventItem(event_id=ev1.id, menu_item_id=m_pannacotta.id, quantity=1, unit_price=m_pannacotta.price_per_head, unit_cost=m_pannacotta.cost_per_head),
        ])
        db.flush()

        # Proposal for ev1
        ev1_total = (9.00 + 29.00 + 8.50) * 85  # $3,952.50
        prop1 = Proposal(
            event_id=ev1.id,
            organization_id=org.id,
            version=1,
            total_amount=ev1_total,
            deposit_percent=30.0,
            status="approved",
            approved_at=datetime.now(timezone.utc) - timedelta(days=25),
        )
        db.add(prop1)

        # Deposit & Balance Invoices for ev1 (Both Paid)
        inv1_dep = Invoice(
            event_id=ev1.id,
            organization_id=org.id,
            kind="deposit",
            amount=round(ev1_total * 0.30, 2),
            due_date=today - timedelta(days=35),
            status="paid",
        )
        inv1_bal = Invoice(
            event_id=ev1.id,
            organization_id=org.id,
            kind="balance",
            amount=round(ev1_total * 0.70, 2),
            due_date=today - timedelta(days=22),
            status="paid",
        )
        db.add_all([inv1_dep, inv1_bal])
        db.flush()

        db.add(Payment(
            invoice_id=inv1_dep.id,
            organization_id=org.id,
            amount=inv1_dep.amount,
            status="succeeded",
            raw_event_id="evt_seed_payment_1",
            paid_at=datetime.now(timezone.utc) - timedelta(days=34),
        ))
        db.add(Payment(
            invoice_id=inv1_bal.id,
            organization_id=org.id,
            amount=inv1_bal.amount,
            status="succeeded",
            raw_event_id="evt_seed_payment_2",
            paid_at=datetime.now(timezone.utc) - timedelta(days=21),
        ))

        # Event 2: Confirmed Event (Upcoming in 10 days)
        ev2 = Event(
            organization_id=org.id,
            location_id=loc2.id,
            client_id=c2.id,
            title="Vance Executive Board Dinner",
            event_date=today + timedelta(days=10),
            start_time="18:00",
            end_time="22:00",
            venue_address="The Grand Penthouse, 88 Wall St",
            headcount=30,
            status="confirmed",
            notes="Deposit paid; final headcount confirmed at 30.",
        )
        db.add(ev2)
        db.flush()

        m_caprese = dishes[1]
        m_ribeye = dishes[5]
        m_lava = dishes[8]
        db.add_all([
            EventItem(event_id=ev2.id, menu_item_id=m_caprese.id, quantity=1, unit_price=m_caprese.price_per_head, unit_cost=m_caprese.cost_per_head),
            EventItem(event_id=ev2.id, menu_item_id=m_ribeye.id, quantity=1, unit_price=m_ribeye.price_per_head, unit_cost=m_ribeye.cost_per_head),
            EventItem(event_id=ev2.id, menu_item_id=m_lava.id, quantity=1, unit_price=m_lava.price_per_head, unit_cost=m_lava.cost_per_head),
        ])
        db.flush()

        ev2_total = (11.00 + 36.00 + 9.50) * 30  # $1,695.00
        prop2 = Proposal(
            event_id=ev2.id,
            organization_id=org.id,
            version=1,
            total_amount=ev2_total,
            deposit_percent=30.0,
            status="approved",
            approved_at=datetime.now(timezone.utc) - timedelta(days=5),
        )
        db.add(prop2)
        inv2_dep = Invoice(
            event_id=ev2.id,
            organization_id=org.id,
            kind="deposit",
            amount=round(ev2_total * 0.30, 2),
            due_date=today - timedelta(days=5),
            status="paid",
        )
        inv2_bal = Invoice(
            event_id=ev2.id,
            organization_id=org.id,
            kind="balance",
            amount=round(ev2_total * 0.70, 2),
            due_date=today + timedelta(days=3),
            status="unpaid",
        )
        db.add_all([inv2_dep, inv2_bal])
        db.flush()

        db.add(Payment(
            invoice_id=inv2_dep.id,
            organization_id=org.id,
            amount=inv2_dep.amount,
            status="succeeded",
            raw_event_id="evt_seed_payment_3",
            paid_at=datetime.now(timezone.utc) - timedelta(days=5),
        ))

        # Event 3: Proposed Event (Awaiting client review/approval)
        ev3 = Event(
            organization_id=org.id,
            location_id=loc1.id,
            client_id=c3.id,
            title="Thorne Autumn Wedding Reception",
            event_date=today + timedelta(days=28),
            start_time="15:00",
            end_time="23:00",
            venue_address="Meadowbrook Botanical Gardens",
            headcount=120,
            status="proposed",
            notes="Client reviewing proposal #1 with custom mocktails.",
        )
        db.add(ev3)
        db.flush()

        m_risotto = dishes[3]
        m_mocktail = dishes[11]
        db.add_all([
            EventItem(event_id=ev3.id, menu_item_id=m_bruschetta.id, quantity=1, unit_price=m_bruschetta.price_per_head, unit_cost=m_bruschetta.cost_per_head),
            EventItem(event_id=ev3.id, menu_item_id=m_salmon.id, quantity=1, unit_price=m_salmon.price_per_head, unit_cost=m_salmon.cost_per_head),
            EventItem(event_id=ev3.id, menu_item_id=m_risotto.id, quantity=1, unit_price=m_risotto.price_per_head, unit_cost=m_risotto.cost_per_head),
            EventItem(event_id=ev3.id, menu_item_id=m_mocktail.id, quantity=1, unit_price=m_mocktail.price_per_head, unit_cost=m_mocktail.cost_per_head),
        ])
        db.flush()

        ev3_total = (9.00 + 29.00 + 24.00 + 7.00) * 120  # $8,280.00
        prop3 = Proposal(
            event_id=ev3.id,
            organization_id=org.id,
            version=1,
            total_amount=ev3_total,
            deposit_percent=30.0,
            status="sent",
            public_token="demo-wedding-token-2026",
            sent_at=datetime.now(timezone.utc),
        )
        db.add(prop3)

        db.commit()
        print("[SUCCESS] Demo data seeded successfully!")
        print("  -> Login: demo@cateriq.com / Password123!")
        print("  -> Public proposal preview token: demo-wedding-token-2026")
        print("  -> Calendar iCal token: demo-calendar-token-apex-2026")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
