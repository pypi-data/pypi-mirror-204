import { VecSpaceClient } from '../src/index'

const PORT = process.env.PORT || '8000'
const URL = 'http://localhost:' + PORT
const vecspace = new VecSpaceClient(URL)

export default vecspace