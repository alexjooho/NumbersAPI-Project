import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import Home from './Home';
import CategoryView from "./CategoryView";

const Stack = createNativeStackNavigator();

export default function App() {

  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
        name="Home"
        component={Home}>
        </Stack.Screen>
        <Stack.Screen
        name="CategoryView"
        component={CategoryView}
        options={({ route }) => ({
          title: route.params.category[0].toUpperCase() +
          route.params.category.slice(1)})}>
        </Stack.Screen>
      </Stack.Navigator>
    </NavigationContainer>
  );
}