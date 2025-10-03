db
test
use University
switched to db University

// insert one student
db.Students.insertOne({})
{
  acknowledged: true,
  insertedId: ObjectId('68dfa40dab9f1421475a001e')
}
db.Students.insertOne({
  student_id : 1,
  name : 'Riju',
  age : 22,
  city : "Kolkata",
  course : "Python",
  marks : 85
})
{
  acknowledged: true,
  insertedId: ObjectId('68dfa49eab9f1421475a001f')
}

// insert multiple students
db.Students.insertMany([
  {student_id: 2, name: "Royal Giant", age: 79, city: "Spell Valey", course: "Defence", marks: 67},
  {student_id: 3, name: "Archer", age: 16, city: "Legendary Arena", course: "Archery", marks: 90},
  {student_id: 4, name: "Pekka", age: 35, city: 'Pekkas Playhouse', course: "Fight", marks: 100},
  {student_id: 5, naem: "Wizard", age: 22, city: 'Legendary Arena', course: "Magic", marks: 100}
])

//find all students
db.Students.find()
{
  _id: ObjectId('68dfa40dab9f1421475a001e')
}
{
  _id: ObjectId('68dfa49eab9f1421475a001f'),
  student_id: 1,
  name: 'Riju',
  age: 22,
  city: 'Kolkata',
  course: 'Python',
  marks: 85
}
{
  _id: ObjectId('68dfa712ab9f1421475a0020'),
  student_id: 2,
  name: 'Royal Giant',
  age: 79,
  city: 'Spell Valey',
  course: 'Defence',
  marks: 67
}
{
  _id: ObjectId('68dfa712ab9f1421475a0021'),
  student_id: 3,
  name: 'Archer',
  age: 16,
  city: 'Legendary Arena',
  course: 'Archery',
  marks: 90
}
{
  _id: ObjectId('68dfa712ab9f1421475a0022'),
  student_id: 4,
  name: 'Pekka',
  age: 35,
  city: 'Pekkas Playhouse',
  course: 'Fight',
  marks: 100
}
{
  _id: ObjectId('68dfa712ab9f1421475a0023'),
  student_id: 5,
  naem: 'Wizard',
  age: 22,
  city: 'Legendary Arena',
  course: 'Magic',
  marks: 100
}

// find one student
db.Students.findOne({name : "Pekka"})
{
  _id: ObjectId('68dfa712ab9f1421475a0022'),
  student_id: 4,
  name: 'Pekka',
  age: 35,
  city: 'Pekkas Playhouse',
  course: 'Fight',
  marks: 100
}

// find stuents with marks > 85
db.Students.find({marks: {$gt : 85}})
{
  _id: ObjectId('68dfa712ab9f1421475a0021'),
  student_id: 3,
  name: 'Archer',
  age: 16,
  city: 'Legendary Arena',
  course: 'Archery',
  marks: 90
}
{
  _id: ObjectId('68dfa712ab9f1421475a0022'),
  student_id: 4,
  name: 'Pekka',
  age: 35,
  city: 'Pekkas Playhouse',
  course: 'Fight',
  marks: 100
}
{
  _id: ObjectId('68dfa712ab9f1421475a0023'),
  student_id: 5,
  naem: 'Wizard',
  age: 22,
  city: 'Legendary Arena',
  course: 'Magic',
  marks: 100
}
// find only name and courses
db.Students.find({}, {name: 1, course: 1, _id : 0})
{}
{
  name: 'Riju',
  course: 'Python'
}
{
  name: 'Royal Giant',
  course: 'Defence'
}
{
  name: 'Archer',
  course: 'Archery'
}
{
  name: 'Pekka',
  course: 'Fight'
}


db.Students.updateOne(
  {name: "Wizard"},
  {$set: {marks: 92, course: "Advanced magic"}}
)
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 0,
  modifiedCount: 0,
  upsertedCount: 0
}

// update multiple
db.Students.updateMany(
  {city: "Legendary Arena"},
  {$set: {grade: 'A'}}
)
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 2,
  modifiedCount: 2,
  upsertedCount: 0
}

// delete one
db.Students.deleteOne({name: "Archer"})
{
  acknowledged: true,
  deletedCount: 1
}

//delete many
db.Students.deleteMany({marks: {$lt : 80}})