import ky, { type KyResponse } from "ky"
import { scrapeState } from "./store.svelte"

export async function startContext() {
  const serviceIndex: number = (document.getElementById("ServiceDisplay") as HTMLSelectElement).selectedIndex
  const storageState: string = (document.getElementById("StorageDisplay") as HTMLSelectElement).value
  const contextURL: string = (document.getElementById("ContextURL") as HTMLInputElement).value
  const autoLogIn: boolean = (document.getElementById("Autologin") as HTMLInputElement).checked
  const sendData = {
    "serviceIndex": serviceIndex,
    "storageState": storageState,
    "contextURL": contextURL,
    "autoLogIn": autoLogIn
  }
  const res: KyResponse = await ky.post("http://localhost:8000/api/appstate", { json: sendData })
  const result = await res.json()
  console.log(result)
  return
}

export async function getServices(): Promise<string[]> {
  interface Response {
    service: string[]
  }
  const res: KyResponse = await ky.get("http://localhost:8000/api/appstate/service")
  const result: Response = await res.json()
  const doc = document.getElementById("ServiceDisplay")
  while (doc && doc.hasChildNodes()) {
    doc.removeChild(doc.children[0]);
  }
  const services: string[] = result?.service;
  for (let service of services) {
    const opt = document.createElement("option");
    opt.setAttribute("value", service);
    opt.innerText = service;
    doc?.appendChild(opt);
  }
  return result.service
}

export async function getStorageStates(): Promise<string[]> {
  interface Response {
    storageState: string[]
  }
  // get states
  const res: KyResponse = await ky.get("http://localhost:8000/api/appstate/storagestate")
  const result: Response = await res.json()

  // set states as options
  const doc = document.getElementById("StorageDisplay");
  while (doc && doc.hasChildNodes()) {
    doc.removeChild(doc.children[0]);
  }
  const states: string[] = result?.storageState;
  for (let state of states) {
    const opt = document.createElement("option");
    opt.setAttribute("value", state);
    opt.innerText = state;
    doc?.appendChild(opt);
  }
  return result.storageState
}
