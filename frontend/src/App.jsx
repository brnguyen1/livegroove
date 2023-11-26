import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from './pages/Home'
import Lobby from "./pages/Lobby";

function App() {

  return (
    <BrowserRouter>
    <Routes>
      <Route index path="/" element={<Home />} />
      <Route exact path="/:session_id" element={<Lobby/>}/>
    </Routes>
  </BrowserRouter>
  )
}

export default App
