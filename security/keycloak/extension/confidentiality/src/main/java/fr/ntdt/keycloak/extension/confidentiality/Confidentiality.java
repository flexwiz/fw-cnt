package fr.sample.keycloak.extension.confidentiality;

import org.keycloak.authentication.RequiredActionContext;
import org.keycloak.authentication.RequiredActionProvider;
import org.keycloak.common.util.Time;

import javax.ws.rs.core.Response;
import java.util.Collections;

public class Confidentiality implements RequiredActionProvider {

    public static final String PROVIDER_ID = "confidentiality";
    private static final String USER_ATTRIBUTE = PROVIDER_ID;


    @Override
    public void evaluateTriggers(RequiredActionContext requiredActionContext) {

    }

    @Override
    public void requiredActionChallenge(RequiredActionContext context) {
        Response challenge = context.form().createForm("confidentiality.ftl");
        context.challenge(challenge);
    }

    @Override
    public void processAction(RequiredActionContext context) {
        if (context.getHttpRequest().getDecodedFormParameters().containsKey("cancel")) {
            context.getUser().removeAttribute(USER_ATTRIBUTE);
            context.failure();
            return;
        }

        context.getUser().setAttribute(USER_ATTRIBUTE, Collections.singletonList(Integer.toString(Time.currentTime())));

        context.success();
    }

    @Override
    public void close() {

    }
}
