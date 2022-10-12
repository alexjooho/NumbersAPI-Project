import React from "react";
import { useEffect, useState } from "react";
import { View, Text, TextInput, ActivityIndicator } from "react-native";
import axios from "axios";

const CategoryView = ({navigation, route}) => {
  const [fact, setFact] = useState({fact: null, isLoading: true});
  const category = route.params.category;


  const getFact = async () => {
    try {
      const response = await axios(`http://192.168.1.87:5001/api/${category}/${text}`)
    }
  }


  if(category === "dates") {

  }
}


export default CategoryView;