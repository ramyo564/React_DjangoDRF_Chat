import axios from "axios";
import { AuthServiceProps } from "../@types/auth-service";
import { useState } from "react";


export function useAuthService(): AuthServiceProps {
    const [isLoggedIn, setIsLoggedIn] = useState<boolean>(()=> {
        const loggedIn = localStorage.getItem("isLoggedId")
        if (loggedIn != null){
            return Boolean(loggedIn)
        } else {
            return false
        }
    })

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
            setIsLoggedIn(true);
            localStorage.setItem("isLoggedIn", "true")
        } catch (err: any) {
            setIsLoggedIn(false)
            localStorage.setItem("isLoggedIn", "false")
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
            localStorage.setItem("isLoggedIn", "true")
            setIsLoggedIn(true)

            getUserDetails()
        } catch (err: any) {
            return err.response.status;
        }
    }
    return {login, isLoggedIn}
}