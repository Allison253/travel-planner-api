from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import engine, Base, get_db
from models import Trip, Activity
from datetime import date

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def root():
    return {"message": "Travel Planner API is running!"}


#trip handling
@app.post("/trips", status_code=201)
async def create_trip(name: str, destination: str, db: AsyncSession = Depends(get_db)):
    trip = Trip(name=name, destination=destination)
    db.add(trip)
    await db.commit()
    await db.refresh(trip)
    return {
        "id": trip.id,
        "name": trip.name,
        "destination": trip.destination
    }

@app.get("/trips")
async def get_trips(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trip))
    trips = result.scalars().all()
    return [
        {
            "id": t.id,
            "name": t.name,
            "destination": t.destination
        }
        for t in trips
    ]


@app.delete("/trips/{trip_id}", status_code=204)
async def delete_trip(trip_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trip).where(Trip.id == trip_id))
    trip = result.scalar_one_or_none()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    await db.delete(trip)
    await db.commit()

    return


#activities handling
@app.post("/activities/{trip_id}", status_code=201)
async def create_activity(trip_id: int, activityname: str, activitydate: date, activityloc: str, activity_price: float, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trip).where(Trip.id == trip_id))
    trip = result.scalar_one_or_none()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    activity=Activity(name=activityname, date = activitydate, location=activityloc, price=activity_price, trip_id=trip_id)
    db.add(activity)
    await db.commit()
    await db.refresh(activity)
    return {
        "id": activity.id,
        "name": activity.name,
        "date": activity.date,
        "location": activity.location,
        "price":activity.price,
        "trip_id": activity.trip_id
    }


@app.get("/activities/{trip_id}")
async def get_activities(trip_id: int,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Activity).where(Activity.trip_id== trip_id))
    activities = result.scalars().all()
    return [
        {
            "id": a.id,
            "name": a.name,
            "date": a.date,
            "location": a.location,
            "price":a.price,
            "trip_id": a.trip_id
        }
        for a in activities
    ]


@app.delete("/activities/{activity_id}", status_code=204)
async def delete_activity(activity_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    a = result.scalar_one_or_none()

    if not a:
        raise HTTPException(status_code=404, detail="Activity not found")

    await db.delete(a)
    await db.commit()

    return


@app.put("/activities/{activity_id}")
async def update_activity(
    activity_id: int,
    name: str | None = None,
    date: date | None = None,
    location: str | None = None,
    price: float | None = None,
    db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Activity).where(Activity.id == activity_id)
    )
    activity = result.scalar_one_or_none()

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    if name is not None:
        activity.name = name
    if date is not None:
        activity.date = date
    if location is not None:
        activity.location = location
    if price is not None:
        activity.price = price

    await db.commit()
    await db.refresh(activity)

    return {
        "id": activity.id,
        "name": activity.name,
        "date": activity.date,
        "location": activity.location,
        "price": activity.price,
        "trip_id": activity.trip_id
    }