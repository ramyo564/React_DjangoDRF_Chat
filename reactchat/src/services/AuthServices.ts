import axios from "axios";
import { AuthServiceProps } from "../@types/auth-service";


export function useAuthService(): AuthServiceProps {

    const getUserDetails = async () => {
        try {
            const userId = localStorage.getItem("userId")
            const accessToken = localStorage.getItem("access_token")
            const response = await axios.get(
                `http://127.0.0.1:8000/api/account/?user_id=${userId}`,{
                    headers:{
                        Authorization: `Bearer ${accessToken}`
                    }
                }
                
            );
            const userDetails = response.data
            localStorage.setItem( "username", userDetails.username );

        } catch (err: any) {
            return err;
        }
    }
    const getUserIdFromToken = (access : string) => {
        const token = access
        const tokenParts = token.split('.')
        const encodedPayLoad = tokenParts[1]
        const decodedPayLoad = atob(encodedPayLoad)
        const payLoadData = JSON.parse(decodedPayLoad)
        const userId = payLoadData.user_id

        return userId
    }
    const login = async (username: string, password: string) => {
        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/api/token/", {
                    username,
                    password,
                }
            );

            const { access, refresh } = response.data;

            // Save the tokens to local storage
            localStorage.setItem( "access_token", access );
            localStorage.setItem( "refresh_token", refresh );
            localStorage.setItem( "userId", getUserIdFromToken(access))

            getUserDetails()
        } catch (err: any) {
            return err;
        }
    }
    return {login}
}