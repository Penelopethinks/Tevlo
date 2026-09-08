from pathlib import Path
p=Path('index.html'); s=p.read_text(encoding='utf-8')
marker='<meta name="tevlo-green-repair" content="1">'
if marker in s:
    raise SystemExit(0)
s=s.replace('<meta name="theme-color" content="#138a5b">','<meta name="theme-color" content="#138a5b">\n'+marker,1)
css='''\nhtml,body{background:#061b12!important;color:#ecfff5!important}\n.auth-wrap{background:radial-gradient(circle at 20% 10%,rgba(57,217,138,.18),transparent 28%),radial-gradient(circle at 90% 80%,rgba(19,138,91,.2),transparent 34%),#061b12!important}\n.auth-card,.sidebar,.main,.chat-head,.composer,.modal,.chat-menu,.message-menu,.reaction-picker,.emoji-panel,.sticker-panel{background:#0d2d20!important;color:#ecfff5!important;border-color:#245641!important}\n.main,.messages{background:linear-gradient(145deg,#071f16,#0b2b1e,#08251a)!important}\ninput,textarea,.search-wrap input,.composer textarea,.settings-card{background:#0a2419!important;color:#ecfff5!important;border-color:#245641!important}\n.tab.active,.theme-choice,.choice-row,.notification-row,.profile-mini,.file-card,.media-card{background:#103625!important;color:#ecfff5!important;border-color:#245641!important}\n.tab,.filter-tab,.ghost{color:#a9d8bd!important}\n.secondary,.icon-btn,.tool-round{background:#123f2c!important;color:#55e69a!important}\n.primary,.send{background:linear-gradient(135deg,#25c978,#0f8b58)!important;color:#f2fff8!important;box-shadow:0 10px 28px rgba(37,201,120,.25)!important}\n.mine .bubble{background:linear-gradient(135deg,#159f63,#0b7448)!important;color:#effff7!important}\n.theirs .bubble{background:#174d37!important;color:#eafff3!important}\n.conv:hover,.user-result:hover,.friend-row:hover,.chat-menu button:hover,.message-menu button:hover,.emoji-panel button:hover,.sticker-panel button:hover{background:#123f2c!important}\n.conv.active,.filter-tab.active,.choice-row.selected{background:#15523a!important;color:#eafff3!important}\n.reaction,.reaction-picker button{background:#123f2c!important;color:#eafff3!important;border-color:#2b654c!important}\n.profile-avatar-wrap{background:#0d2d20!important}.icon-badge{border-color:#0d2d20!important}.switch:after{background:#c9f6dc!important}\nbutton{transition:transform .12s ease,filter .12s ease,box-shadow .12s ease}button:hover{filter:brightness(1.08)}button:active{transform:scale(.96)!important}button:focus-visible{outline:3px solid #39d98a!important;outline-offset:2px!important}\n'''
s=s.replace('</style>',css+'</style>',1)
js=r'''
let tevloSending=false;
async function tevloReliableSend(){
 if(tevloSending)return;
 if(!SUPABASE_READY){if(typeof sendCurrent==='function')return sendCurrent();return;}
 const input=$("#composerText"),c=state.conversations?.find(x=>x.id===state.active),body=(input?.value||"").trim();
 if(!input||!c||!body)return;
 tevloSending=true;const btn=$("#sendBtn");if(btn){btn.disabled=true;btn.textContent="…";}
 try{const ttl=state.disappear?.[c.id]||0;const {error}=await sb.from("tevlo_messages").insert({conversation_id:c.id,sender_id:state.user.id,body,type:"text",reply_to_id:state.replyTo||null,expires_at:ttl?new Date(Date.now()+ttl*1000).toISOString():null});if(error)throw error;input.value="";if(state.drafts){delete state.drafts[c.id];localStorage.setItem("tevlo_drafts",JSON.stringify(state.drafts));}state.replyTo=null;input.placeholder="Message";if(typeof autoSize==='function')autoSize();await openConversation(c.id)}catch(err){console.error(err);toast("Could not send: "+(err?.message||"Please try again."))}finally{tevloSending=false;if(btn){btn.disabled=false;btn.textContent="↑";}}}

document.addEventListener("click",async e=>{const b=e.target.closest("button,[data-conv],[data-person],[data-filter]");if(!b)return;const id=b.id;
 if(id==="sendBtn"){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();await tevloReliableSend();return}
 if(id==="newChat"||id==="emptyNew"){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();newChatModal();return}
 if(id==="peopleBtn"){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();peopleModal();return}
 if(id==="profileBtn"){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();profileModal();return}
 if(id==="settingsBtn"){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();settingsModal();return}
 if(id==="notificationsBtn"){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();notificationsModal();return}
 if(id==="requestsBtn"){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();requestsModal();return}
 const conv=b.closest("[data-conv]");if(conv){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();openConversation(conv.dataset.conv);return}
 const person=b.closest("[data-person]");if(person){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();startConversation(person.dataset.person);return}
 const filter=b.closest("[data-filter]");if(filter){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();state.filter=filter.dataset.filter;document.querySelectorAll('.filter-tab').forEach(x=>x.classList.toggle('active',x===filter));renderConversationList();return}
 const call={
 backBtn:()=>document.querySelector('.shell')?.classList.remove('chat-open'),
 searchChatBtn:()=>{$('#chatSearchBar')?.classList.remove('hidden');$('#chatSearchInput')?.focus()},
 closeChatSearch:()=>{$('#chatSearchBar')?.classList.add('hidden');if($('#chatSearchInput'))$('#chatSearchInput').value='';renderMessages()},
 plusBtn:()=>{$('#emojiPanel')?.classList.toggle('hidden');$('#stickerPanel')?.classList.add('hidden')},
 stickerBtn:()=>{$('#stickerPanel')?.classList.toggle('hidden');$('#emojiPanel')?.classList.add('hidden')},
 mediaBtn:()=>$('#mediaInput')?.click(),recordBtn:()=>toggleRecorder(),chatMenuBtn:()=>$('#chatMenu')?.classList.toggle('hidden'),favoriteBtn:()=>toggleFavorite(state.active),pinBtn:()=>togglePin(state.active),
 themeBtn:()=>{const c=state.conversations?.find(x=>x.id===state.active);if(c)themeModal(c)},disappearBtn:()=>{const c=state.conversations?.find(x=>x.id===state.active);if(c)disappearModal(c)},
 clearDraft:()=>{const c=state.conversations?.find(x=>x.id===state.active);if(c){delete state.drafts[c.id];localStorage.setItem('tevlo_drafts',JSON.stringify(state.drafts));if($('#composerText'))$('#composerText').value='';autoSize();toast('Draft cleared.')}},
 muteChat:()=>toast('Conversation muted.'),removeFriend:()=>{const c=state.conversations?.find(x=>x.id===state.active);if(c)removeFriend(c)},blockUser:()=>{const c=state.conversations?.find(x=>x.id===state.active);if(c)blockUser(c)},reportUser:()=>{const c=state.conversations?.find(x=>x.id===state.active);if(c)reportUser(c)}};
 if(call[id]){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();call[id]();return}
},true);
document.addEventListener("keydown",e=>{if(e.target?.id==="composerText"&&e.key==="Enter"&&!e.shiftKey){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();tevloReliableSend()}},true);
'''
s=s.replace('\n})();\n</script>',js+'\n})();\n</script>',1)
p.write_text(s,encoding='utf-8')
