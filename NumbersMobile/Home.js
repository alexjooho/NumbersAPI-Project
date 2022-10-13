import React from "react";
import { useEffect, useState } from "react";
import { StyleSheet, View, Text, Button, ActivityIndicator } from "react-native";
import axios from "axios";
import { StatusBar } from "expo-status-bar";
import { BASE_URL } from "@env";

const Home = ({ navigation }) => {
  const [isLoading, setLoading] = useState(true);
  const [data, setData] = useState("");

  const getRandomFact = async () => {
    try {
      const response = await axios(`${BASE_URL}/api/trivia/random`);
      // the BASE_URL in the .env file needs to be changed whenever a new ngrok url is given
      setData(response.data.fact.statement);
    }
    catch (error) {
      setData("An error has occurred");
    }
    finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getRandomFact();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to NumbersAPI!</Text>
      <View style={styles.buttonView}>
        <Button title="Trivia" onPress={() => navigation.push("CategoryView",
          { category: "trivia" })}/>
        <Button title="Dates" onPress={() => navigation.push("CategoryView",
          { category: "dates" })}/>
        <Button title="Years" onPress={() => navigation.push("CategoryView",
          { category: "years" })}/>
        <Button title="Math" onPress={() => navigation.push("CategoryView",
          { category: "math" })}/>
      </View>
      <Text style={styles.randomFact}>Here is your random fact of the day!</Text>
      {isLoading ? <ActivityIndicator /> : (
        <Text style={styles.data}>{data}</Text>
      )}
      <StatusBar style="auto" />
      <View style={styles.newFact}>
        <Button title="Get another fact" onPress={getRandomFact} color="darkviolet"/>
      </View>
      <Text style={styles.api}>You can view the NumbersAPI docs at numbersapi.com</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "lightcyan",
    alignItems: "center",
  },
  title: {
    color: "cornflowerblue",
    fontSize: 30,
    fontWeight: "bold",
    marginTop: 20,
    padding: 5
  },
  buttonView: {
    margin: 10,
    flexDirection: "row",
    justifyContent: "space-between"
  },
  randomFact: {
    color: "darkorange",
    fontSize: 25,
    marginTop: 30,
  },
  data: {
    fontSize: 20,
    padding: 10,
    marginTop: 15,
    backgroundColor: "wheat"
  },
  newFact: {
    marginTop: 30
  },
  api: {
    fontSize: 15,
    color: "slategrey",
    marginTop: 40
  }

});


export default Home;