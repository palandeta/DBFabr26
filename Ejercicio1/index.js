import express from 'express'
import mongoose from 'mongoose'

const alumno = mongoose.model('Alumno', new mongoose.Schema({
	    cedula: String,
	    nombre: String
}))

const app = express()

mongoose.connect('mongodb://pablo:pablo1234@cont_mongo_pablo:27017/bdalumnos?authSource=admin')

app.get('/', async (req,res) => {
	    console.log('Listando alumnos ...')
	    const alumnos = await alumno.find();
	    return res.send(alumnos)
})

app.get('/crear', async (req,res) => {
	    console.log('Creando alunmo ...')
	    await alumno.create({cedula:'1002161055', nombre: 'Pablo'})
	    return res.send('ok')
})

app.listen(3000, () => console.log('Servidor ejecutandose ..'))
