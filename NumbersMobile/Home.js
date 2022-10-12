import React from "react";
import { useEffect, useState } from "react";
import { View, Text, Button, ActivityIndicator } from "react-native";
import axios from "axios";
import { StatusBar } from "expo-status-bar";

const Home = ({navigation}) => {
  const [isLoading, setLoading] = useState(true);
  const [data, setData] = useState("");

  const getRandomFact = async () => {
    try {
      console.log("entering try block")
      // const response = await axios("http://numbersapi.com/23/trivia?fragment");
      const response = await axios("http://192.168.1.87:5001/api/trivia/random");
      console.log("json:", response.data.fact.statement)
      setData(response.data.fact.statement);
    }
    catch (error) {
      console.log(error);
    }
    finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    getRandomFact();
  }, [])

  return (
    <View style={styles.container}>
      <Button title="Trivia" onPress={() => navigation.push("CategoryView",
      {category: "trivia"})}/>
      <Button title="Dates" onPress={() => navigation.push("CategoryView",
      {category: "dates"})}/>
      <Button title="Years" onPress={() => navigation.push("CategoryView",
      {category: "years"})}/>
      <Button title="Math" onPress={() => navigation.push("CategoryView",
      {category: "math"})}/>
      <Text>Here is your random fact of the day!</Text>
      {isLoading ? <ActivityIndicator/> : (
        <Text>{data}</Text>
      ) }
      <StatusBar style="auto" />
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
});


export default Home;