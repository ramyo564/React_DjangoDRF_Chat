
import Home from "./pages/Home"
import Server from "./pages/Server"
import Explore from "./pages/Explore";
import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider } from "react-router-dom"
import ToggleColorMode from "./components/ToggleColorMode";
import Login from "./pages/Login";
import { AuthServicProvicer } from "./context/AuthContext";
import TestLogin from "./pages/TestLogin";
import ProtectedRoute from "./services/ProtectedRoute";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route>
      <Route path="/" element={<Home/>} />
      <Route path="/server/:serverId/:channelId?" element={<Server />} />
      <Route path="/explore/:categoryName" element={<Explore />} />
      <Route path="/login" element={<Login/>} />
      <Route 
        path="/testlogin"
        element={
          <ProtectedRoute>
            <TestLogin/>
          </ProtectedRoute>
        } 
      />
    </Route>
  )
);

const App = () => {

  return (
    <AuthServicProvicer>
      <ToggleColorMode>
        <RouterProvider router={router} />
      </ToggleColorMode>
    </AuthServicProvicer>
  );
};

export default App;
