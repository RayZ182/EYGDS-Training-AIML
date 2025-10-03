use University
switched to db University

db.Teachers.insertMany([
  {teacher_id: 1, name: "Soumen", subject: "English", salary: 50000},
  {teacher_id: 2, name: "Sangita", subject: "Chemistry", salary: 60000},
  {teacher_id: 3, name: "Soumya", subject: "Math", salary: 65000},
  {teacher_id: 4, name: "Rumi", subject: "History", salary: 45000}
])
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId('68dfb51be51a08cfdcaeb119'),
    '1': ObjectId('68dfb51be51a08cfdcaeb11a'),
    '2': ObjectId('68dfb51be51a08cfdcaeb11b'),
    '3': ObjectId('68dfb51be51a08cfdcaeb11c')
  }
}
db.Teachers.find()
{
  _id: ObjectId('68dfb51be51a08cfdcaeb119'),
  teacher_id: 1,
  name: 'Soumen',
  subject: 'English',
  salary: 50000
}
{
  _id: ObjectId('68dfb51be51a08cfdcaeb11a'),
  teacher_id: 2,
  name: 'Sangita',
  subject: 'Chemistry',
  salary: 60000
}
{
  _id: ObjectId('68dfb51be51a08cfdcaeb11b'),
  teacher_id: 3,
  name: 'Soumya',
  subject: 'Math',
  salary: 65000
}
{
  _id: ObjectId('68dfb51be51a08cfdcaeb11c'),
  teacher_id: 4,
  name: 'Rumi',
  subject: 'History',
  salary: 45000
}
db.Teachers.find(
  {},{name: 1, subject: 1, _id: 0}
)
{
  name: 'Soumen',
  subject: 'English'
}
{
  name: 'Sangita',
  subject: 'Chemistry'
}
{
  name: 'Soumya',
  subject: 'Math'
}
{
  name: 'Rumi',
  subject: 'History'
}
db.Teachers.updateMany(
  {subject: "History"},
  {$set: {salary: 25000}}
)
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}
db.Teachers.deleteOne({salary: {$lt: 30000}})

db.Teachers.insertMany([
  {teacher_id: 1, name: "Soumen", subject: "English", salary: 50000},
  {teacher_id: 2, name: "Sangita", subject: "Chemistry", salary: 60000},
  {teacher_id: 3, name: "Soumya", subject: "Math", salary: 65000},
  {teacher_id: 4, name: "Rumi", subject: "History", salary: 45000}
])
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId('68dfb51be51a08cfdcaeb119'),
    '1': ObjectId('68dfb51be51a08cfdcaeb11a'),
    '2': ObjectId('68dfb51be51a08cfdcaeb11b'),
    '3': ObjectId('68dfb51be51a08cfdcaeb11c')
  }
}
db.Teachers.find()
{
  _id: ObjectId('68dfb51be51a08cfdcaeb119'),
  teacher_id: 1,
  name: 'Soumen',
  subject: 'English',
  salary: 50000
}
{
  _id: ObjectId('68dfb51be51a08cfdcaeb11a'),
  teacher_id: 2,
  name: 'Sangita',
  subject: 'Chemistry',
  salary: 60000
}
{
  _id: ObjectId('68dfb51be51a08cfdcaeb11b'),
  teacher_id: 3,
  name: 'Soumya',
  subject: 'Math',
  salary: 65000
}
{
  _id: ObjectId('68dfb51be51a08cfdcaeb11c'),
  teacher_id: 4,
  name: 'Rumi',
  subject: 'History',
  salary: 45000
}
db.Teachers.find(
  {},{name: 1, subject: 1, _id: 0}
)
{
  name: 'Soumen',
  subject: 'English'
}
{
  name: 'Sangita',
  subject: 'Chemistry'
}
{
  name: 'Soumya',
  subject: 'Math'
}
{
  name: 'Rumi',
  subject: 'History'
}
db.Teachers.updateMany(
  {subject: "History"},
  {$set: {salary: 25000}}
)
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}
db.Teachers.deleteOne({salary: {$lt: 30000}})
