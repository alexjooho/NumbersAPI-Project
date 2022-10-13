import React from "react";
import { useState } from "react";
import { StyleSheet, View, Text, TextInput, Keyboard, TouchableWithoutFeedback } from "react-native";
import axios from "axios";
import { BASE_URL } from "@env";

const CategoryView = ({ navigation, route }) => {

  const [fact, setFact] = useState("");
  const [input, setInput] = useState("");

  const category = route.params.category;

  let promptText;

  if (category === "trivia" || category === "math") {
    promptText = `Enter a number (e.g. "5") or "random" to get a ${category} fact!`;
  }

  else if (category === "years") {
    promptText = 'Enter a year (e.g. "1970") or "random" to get a year fact!';
  }

  else if (category === "dates") {
    promptText =
      `Enter a valid month/day together (e.g. "10/4") or "random" to get a date fact!`;
  }

  async function getFact(text) {
    try {
      // const response = await axios(`https://43ab-2603-8000-8844-a041-54e2-4dc3-95ec-96bb.ngrok.io/api/${category}/${text}`);
      const response = await axios(`${BASE_URL}/api/${category}/${text}`);
      setFact(response.data.fact.statement);
    }
    catch (error) {
      if (error.response.data.error) {
        setFact(error.response.data.error.message);
      }
      else {
        setFact("Uh oh, we don't understand that URL.");
      }
    }
  }

  return (
    <TouchableWithoutFeedback onPress={Keyboard.dismiss} accessible={false}>
      <View style={styles.container}>
        <Text style={styles.prompt}>{promptText}</Text>
        <TextInput
          style={styles.input}
          placeholder="Type here for a fact!"
          onChangeText={newText => setInput(newText)}
          onSubmitEditing={() => { getFact(input); }}>
        </TextInput>
        {fact
          ? <Text style={styles.fact}>{fact}</Text>
          : null}
      </View>
    </TouchableWithoutFeedback>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "lightcyan",
    alignItems: "center",
  },
  prompt: {
    color: "cornflowerblue",
    fontSize: 30,
    marginTop: 30,
    padding: 5
  },
  input: {
    height: 200,
    fontSize: 40,
    padding: 10,
    color: "red"
  },
  fact: {
    padding: 10,
    color: "darkorange",
    fontSize: 30,
  }
});

export default CategoryView;