import { useAuthServiceContext } from "../context/AuthContext";

const TestLogin = () => {
    const { isLoggedIn } = useAuthServiceContext();
    return <>{isLoggedIn.toString()}</>;
};

export default TestLogin;