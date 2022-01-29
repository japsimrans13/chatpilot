// Require the framework and instantiate it
const fastify = require('fastify')({ logger: true })
const { nanoid } = require("nanoid");
// Declare a route
fastify.get('/', async (request, response) => {
  response.send({ hello: 'everything still fine' });
})

let greetings = [
  { message: "Hello! How can I help you?" },
  { message: "Hello! How are you doing? I will be assisting you today." },
  { message: "Hi! Tell me, how can I help?" },
  { message: "Greetings! Is everything ok?" }
];
let apologies = [
  { message: "I'm sorry to hear that" },
  { message: "Oh no! I'm sorry about that" },
  { message: "That's bad! Definitely not the experience we want to provide!" }
];
let solutions = [
  { message: "You can exchange the value of the item for in-app credits" },
  { message: "You can get a refund" },
  { message: "You can change the item for another one" }
];

let tickets = [];

// GET /greeting
fastify.get('/greetings', async (request, response) => {
   //Returns array of greetings
   response.send(greetings);
})
// GET /apology
fastify.get('/apology', async (request, response) => {
  //Returns array of apologies
  response.send(apologies);
})

// GET /solutions
fastify.get('/solutions', async (request, response) => {
  response.send(solutions);
})

// POST /ticket
fastify.post('/ticket', async (request, response) => {
  const newTicket = request.body;
  console.log(newTicket);
  //newTicket.id = nanoid();
  tickets.push(newTicket);
  response.code(201).send(newTicket);
})

// Run the server!
const start = async () => {
  try {
    await fastify.listen(3000)
  } catch (err) {
    fastify.log.error(err)
    process.exit(1)
  }
}
start()